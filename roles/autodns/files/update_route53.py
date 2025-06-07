#!/usr/bin/env python

import datetime
from ipaddress import ip_address, IPv4Address, IPv6Address
import json
import logging
import os
from pathlib import Path
import subprocess
import time

import boto3

### CONFIG ###
## Any of these values can be overridden with environment variables at ##
## call time.  The ones without a default are required values.         ##

# Hosted Zone ID e.g. BJBK35SKMM9OE
# Note, this value is required to be set as an environment variable
R53_ZONEID = os.getenv("R53_ZONEID")

# The CNAME you want to update e.g. hello.example.com
# Note, this value is required to be set as an environment variable
R53_RECORDSET = os.getenv("R53_RECORDSET")

# The Time-To-Live of this recordset
R53_TTL = int(os.getenv("R53_TTL", 300))

# Change this if you want
R53_COMMENT = os.getenv("R53_COMMENT", "")

# Are we doing "A" records, "AAAA" records, or "both"?
R53_TYPE = os.getenv("R53_TYPE", "both")

# Where should the log content write to?
_LOGDIR = Path(os.getenv("LOGDIR", "/var/log/update_route53"))
_LOGFILENAME = Path(os.getenv("LOGFILENAME", "update_route53.log"))
LOGFILE = _LOGDIR / _LOGFILENAME

# Where should the IP value's current value be cached to?
_IPDIR = Path(os.getenv("IPDIR", "/etc/update_route53"))
_IPFILENAME = Path(os.getenv("IPFILENAME", "update_route53.ip"))
IPFILE = _IPDIR / _IPFILENAME

# How many seconds should we wait between loops of this script?
# the value 0 has a special meaning - don't loop, just run once and exit
LOOP_DELAY = int(os.getenv("LOOP_DELAY", 300))

# What log level should the script operate at?  Can be:
# DEBUG, INFO, WARNING, ERROR, or CRITICAL
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

logging.basicConfig(
    level=LOG_LEVEL.upper(),
    filename=LOGFILE,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S%z",
)
logger = logging.getLogger(__name__)


type IPAddress = IPv4Address | IPv6Address


class IpFile:
    """Handle storing the last known IP address of either ipv4 or ipv6 type."""

    def __init__(self, file_path: Path) -> None:
        self.file = file_path
        if not self.file.exists():
            logger.debug(f"Creating new file at {self.file}")
            self.file.write_text(json.dumps({"ipv4": None, "ipv6": None}))

    def _get_json_index_from_address(self, address: IPAddress) -> str:
        match address:
            case IPv6Address():
                return "ipv6"
            case IPv4Address():
                return "ipv4"

    def address_matches(self, address: IPAddress) -> bool:
        """Is the given address the same as the one in the file?"""
        with self.file.open("r") as f:
            body = json.load(f)
        index = self._get_json_index_from_address(address)
        if str(address) != body[index]:
            logger.debug(f"File mismatch: file({body[index]}) != given({str(address)})")
            return False
        logger.debug(f"File match: file({body[index]}) == given({str(address)})")
        return True

    def store_address(self, address: IPAddress) -> None:
        """Write the given address into the file."""
        with self.file.open("r") as f:
            body = json.load(f)
        index = self._get_json_index_from_address(address)
        body[index] = str(address)
        logger.info(f"Updating file for address {address}")
        self.file.write_text(json.dumps(body))


def get_public_address[T: (IPv4Address, IPv6Address)](type: type[T]) -> T:
    """Given an ipaddress type, return the public IP address for this network of that type."""
    result = subprocess.run(
        [
            "/usr/bin/dig",
            f"-{'4' if type is IPv4Address else '6'}",
            "TXT",
            "+short",
            "o-o.myaddr.l.google.com",
            "@ns1.google.com",
        ],
        capture_output=True,
        check=True,
    )
    addr = ip_address(result.stdout.decode("utf-8").replace('"', "").replace("\n", ""))
    if not isinstance(addr, type):
        raise TypeError(f"IP address must be an {type}, got {addr.__class__}")
    logger.debug(f"Got address: {addr}")
    return addr  # type: ignore


def update_dns_record(address: IPAddress) -> None:
    logger.debug(f"Attempting Route53 update for address {address}")
    match address:
        case IPv6Address():
            r53_type = "AAAA"
        case IPv4Address():
            r53_type = "A"

    client = boto3.client("route53")
    client.change_resource_record_sets(
        HostedZoneId=R53_ZONEID,
        ChangeBatch={
            "Comment": f"Auto updating @ {datetime.datetime.now()}",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": R53_RECORDSET,
                        "Type": r53_type,
                        "TTL": R53_TTL,
                        "ResourceRecords": [
                            {"Value": str(address)},
                        ],
                    },
                },
            ],
        },
    )
    logger.info(f"Updated Route53 for address {address}")


if __name__ == "__main__":
    ip_file = IpFile(IPFILE)

    while True:
        try:
            if R53_TYPE in ["A", "both"]:
                addr = get_public_address(IPv4Address)
                if not ip_file.address_matches(addr):
                    update_dns_record(addr)
                    ip_file.store_address(addr)

            if R53_TYPE in ["AAAA", "both"]:
                addr = get_public_address(IPv6Address)
                if not ip_file.address_matches(addr):
                    update_dns_record(addr)
                    ip_file.store_address(addr)

        except Exception as e:
            logger.exception(e)
            if LOOP_DELAY <= 0:
                exit(1)

        finally:
            logger.info("Success.")
            if LOOP_DELAY <= 0:
                exit()
            time.sleep(LOOP_DELAY)

#!/usr/bin/env bash

###
# A simple dynamic DNS solution.
#
# Given a Route53 Zone ID and Record set, read the current
# public IP address of this host and ensure that the Route 53
# record is up to date.
#
# If LOOP_DELAY is greater than 0, run forever as a loop with
# LOOP_DELAY as the number of seconds between executions.
#
# Note that you should provision a specific IAM key for this job,
# and scope the allowed actions to:
#                "route53:GetHostedZone",
#                "route53:ChangeResourceRecordSets",
#                "route53:ListResourceRecordSets"
# And limit the resource to just the appropriate zone id:
#                "arn:aws:route53:::hostedzone/[HOSTED ZONE ID]"
#
# Thanks to:
# https://gist.github.com/phybros/827aa561a44032dd1556
###


### CONFIG ###
## Any of these values can be overridden with environment variables at ##
## call time.  The ones with :? in them are required values.           ##

# Hosted Zone ID e.g. BJBK35SKMM9OE
# Note, this value is required to be set as an environment variable
R53_ZONEID="${R53_ZONEID:?}"

# The CNAME you want to update e.g. hello.example.com
# Note, this value is required to be set as an environment variable
R53_RECORDSET="${R53_RECORDSET:?}"

# The Time-To-Live of this recordset
R53_TTL="${R53_TTL:-300}"

# Change this if you want
R53_COMMENT="${R53_COMMENT:-Auto updating @ `date`}"

# Would be AAAA if it were an ipv6 record, but
# note that the valid_ip() check below only passes ipv4 addresses
R53_TYPE="${R53_TYPE:-A}"

# Where should the log content write to?
LOGDIR="${LOGDIR:-/var/log/update_route53}"
LOGFILENAME="${LOGFILENAME:-update_route53.log}"

# Where should the IP value's current value be cached to?
IPDIR="${IPDIR:-/etc/update_route53}"
IPFILENAME="${IPFILENAME:-update_route53.ip}"

# How many seconds should we wait between loops of this script?
# the value 0 has a special meaning - don't loop, just run once and exit
LOOP_DELAY="${LOOP_DELAY:-300}"

### END CONFIG ###


# Is the passed parameter a valid IPv4 address or not?
function valid_ip() {
    local ip=$1

    local stat=1
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 \
            && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi

    return $stat
}

function writelog() {
    local str=$1
    echo "`date --rfc-3339=seconds`: ${str}" >> "${LOGFILE}"
}

# Handle the end-of-loop logic.
# If the LOOP_DELAY global is greater than 0, then we'll sleep
# for that many seconds and return.  Otherwise, we'll exit.
# The passed parameter is the exit code, if we end up needing it.
function endloop() {
  local exitcode=$1
  if [ $LOOP_DELAY -gt 0 ]; then
      sleep $LOOP_DELAY
  else
      exit $exitcode
  fi
}

set -x

# Set up the state file and log file
LOGFILE="${LOGDIR}/${LOGFILENAME}"
if [ ! -f "$LOGFILE" ]; then
    touch "$LOGFILE"
fi

IPFILE="${IPDIR}/${IPFILENAME}"
if [ ! -f "$IPFILE" ]; then
    touch "$IPFILE"
fi

while true; do

  # Get the external IP address from OpenDNS (more reliable than other providers)
  IP=`dig +short myip.opendns.com @resolver1.opendns.com`
  if ! valid_ip $IP; then
      writelog "ERROR - Invalid IP address: $IP"
      endloop 1 && continue
  fi

  # If the just-read IP address is the same as the one in the state file,
  # log this condition and we're done.
  if grep -Fxq "$IP" "$IPFILE"; then
      writelog "DONE - IP is still $IP"
      endloop 0 && continue
  fi

  # Otherwise, proceed with the DNS update
  TMPFILE=$(mktemp /tmp/temporary-file.XXXXXXXX)
  cat > ${TMPFILE} << EOF
{
  "Comment":"${R53_COMMENT}",
  "Changes":[
    {
      "Action":"UPSERT",
      "ResourceRecordSet":{
        "ResourceRecords":[
          {
            "Value":"${IP}"
          }
        ],
        "Name":"${R53_RECORDSET}",
        "Type":"${R53_TYPE}",
        "TTL":${R53_TTL}
      }
    }
  ]
}
EOF
  cat $TMPFILE

  writelog "IP has changed to $IP, updating"
  AWS_STDOUT=`aws route53 change-resource-record-sets \
      --hosted-zone-id "$R53_ZONEID" \
      --change-batch file://"$TMPFILE"`
  AWS_RETCODE=$?
  writelog $AWS_STDOUT

  rm $TMPFILE

  if [ $AWS_RETCODE -ne 0 ]; then
      writelog "ERROR - AWS call failed with return code: $AWS_RETCODE"
      endloop 1 && continue
  fi

  echo "$IP" > "$IPFILE"
  endloop 0 && continue
done

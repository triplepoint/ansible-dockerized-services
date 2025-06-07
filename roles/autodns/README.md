# Intro
This role installs and configures a job for periodically detecting changes to this server's public IP address and updating an AWS Route53 zone definition to match.

Thanks to Will Warren for developing the script originally used in this job:
https://willwarren.com/2014/07/03/roll-dynamic-dns-service-using-amazon-route53/

## Requirements

## Role Variables
See the [comment in the default variables file](defaults/main.yml) for information on configuration.

## Dependencies
None.

## Example Playbook
    - hosts: whatever
      roles:
        - triplepoint.dockerized_services.autodns

## License
MIT

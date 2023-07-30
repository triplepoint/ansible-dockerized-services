# Intro
This role installs and configures a job for periodically detecting changes to this server's public IP address and updating an AWS Route53 zone definition to match.

Thanks to Will Warren for developing the script used in this job:
https://willwarren.com/2014/07/03/roll-dynamic-dns-service-using-amazon-route53/

## Requirements
While there's no explicit dependency roles, the target machine should be able to act as a Docker host.  The `geerlingguy.docker` Ansible role is a suitable solution.

## Role Variables
See the [comment in the default variables file](defaults/main.yml) for information on configuration.

## Dependencies
None.

## Example Playbook
    - hosts: whatever
      roles:
        - triplepoint.autodns

## License
MIT

# Intro
This role installs and configures a Dockerized Mozilla Sync Server application.
Based heavily on https://github.com/dan-r/syncstorage-rs-docker

## Requirements
While there's no explicit dependency roles, the target machine should be able to act as a Docker host.  The `geerlingguy.docker` Ansible role is a suitable solution.

## Role Variables
See the [comment in the default variables file](defaults/main.yml) for information on configuration.

## Dependencies
None.

## Example Playbook
    - hosts: whatever
      roles:
        - triplepoint.dockerized_services.mozilla_syncserver_rs

## License
MIT

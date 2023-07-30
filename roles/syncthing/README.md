# Intro
This role installs and configures the Syncthing service, suitable for syncing files securely between machines.

## Requirements
None

## Role Variables
See the [comment in the default variables file](defaults/main.yml) for information on configuration.

## Dependencies
None.

## Example Playbook
    - hosts: whatever
      roles:
        - triplepoint.dockerized_services.syncthing

## License
MIT

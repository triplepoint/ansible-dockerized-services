# Intro

This role is intended to be included by other roles, and configured to install arbitary docker services with docker-compose.

## Requirements

While there's no explicit dependency roles, the target machine should be able to act as a Docker host. The `geerlingguy.docker` Ansible role is a suitable solution.

## Role Variables

See the [comment in the default variables file](defaults/main.yml) for information on configuration.

## Dependencies

None.

## Example Usage

In another role, you can:

```
- name: Deploy and start the Docker Compose-managed service
  ansible.builtin.include_role:
    name: triplepoint.dockerized_services.docker_service
  vars:
    docker_service_name: some_service_name
    docker_service_container_name: some/dockerimage
```

See the [default variables file](defaults/main.yml) for more information on the variables you might want to override here.

## License

MIT

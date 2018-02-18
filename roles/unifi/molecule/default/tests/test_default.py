import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_docker_service_enabled(host):
    service = host.service('docker')
    assert service.is_enabled


def test_docker_service_running(host):
    service = host.service('docker')
    assert service.is_running


@pytest.mark.parametrize('socket_def', [
    # all IPv4 tcp sockets on port 8880
    ('tcp://8880'),
])
def test_listening_sockets(host, socket_def):
    socket = host.socket(socket_def)
    assert socket.is_listening

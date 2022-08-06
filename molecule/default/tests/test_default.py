import pytest
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_service(host):
    prom = host.service("prometheus")
    assert prom.is_running
    assert prom.is_enabled

@pytest.mark.parametrize("dirs", [
    "/opt/prometheus",
    "/opt/prometheus/data",
    "/etc/prometheus"
])
def test_dir(host, dirs):
    dir = host.file(dirs)
    assert dir.is_directory
    assert dir.exists

def test_socket(host):
    sock = host.socket("tcp://0.0.0.0:9090")
    assert sock.is_listening

def test_user(host):
    u = host.user("prometheus")
    assert u.exists

def test_group(host):
    g = host.group("prometheus")
    assert g.exists
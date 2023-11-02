# -*- coding: utf-8 -*-

import os
import pytest

from distronode_runner.config.inventory import InventoryConfig
from distronode_runner.config._base import BaseExecutionMode
from distronode_runner.exceptions import ConfigurationError
from distronode_runner.utils import get_executable_path


def test_distronode_inventory_init_defaults(tmp_path, patch_private_data_dir):
    # pylint: disable=W0613
    rc = InventoryConfig()

    # Check that the private data dir is placed in our default location with our default prefix
    # and has some extra uniqueness on the end.
    base_private_data_dir = tmp_path.joinpath('.distronode-runner-').as_posix()
    assert rc.private_data_dir.startswith(base_private_data_dir)
    assert len(rc.private_data_dir) > len(base_private_data_dir)

    assert rc.execution_mode == BaseExecutionMode.DISTRONODE_COMMANDS


def test_invalid_runner_mode_value():
    with pytest.raises(ConfigurationError) as exc:
        InventoryConfig(runner_mode='test')

    assert "Invalid runner mode" in exc.value.args[0]


def test_prepare_inventory_command():
    rc = InventoryConfig()
    inventories = ['/tmp/inventory1', '/tmp/inventory2']
    rc.prepare_inventory_command('list', inventories, response_format='yaml', playbook_dir='/tmp',
                                 vault_ids='1234', vault_password_file='/tmp/password')
    expected_command = [get_executable_path('distronode-inventory'), '--list', '-i', '/tmp/inventory1', '-i', '/tmp/inventory2', '--yaml', '--playbook-dir'] + \
                       ['/tmp', '--vault-id', '1234', '--vault-password-file', '/tmp/password']
    assert rc.command == expected_command
    assert rc.runner_mode == 'subprocess'


def test_prepare_inventory_invalid_action():
    with pytest.raises(ConfigurationError) as exc:
        rc = InventoryConfig()
        inventories = ['/tmp/inventory1', '/tmp/inventory2']
        rc.prepare_inventory_command('test', inventories=inventories)

    assert "Invalid action test, valid value is one of either graph, host, list" == exc.value.args[0]


def test_prepare_inventory_invalid_response_format():
    with pytest.raises(ConfigurationError) as exc:
        rc = InventoryConfig()
        inventories = ['/tmp/inventory1', '/tmp/inventory2']
        rc.prepare_inventory_command('list', inventories=inventories, response_format='test')

    assert "Invalid response_format test, valid value is one of either json, yaml, toml" == exc.value.args[0]


def test_prepare_inventory_invalid_inventories():
    with pytest.raises(ConfigurationError) as exc:
        rc = InventoryConfig()
        inventories = '/tmp/inventory1'
        rc.prepare_inventory_command('list', inventories=inventories)

    assert "inventories should be of type list" in exc.value.args[0]


def test_prepare_inventory_invalid_host_action():
    with pytest.raises(ConfigurationError) as exc:
        rc = InventoryConfig()
        inventories = ['/tmp/inventory1', '/tmp/inventory2']
        rc.prepare_inventory_command('host', inventories=inventories)

    assert "Value of host parameter is required when action in 'host'" == exc.value.args[0]


def test_prepare_inventory_invalid_graph_response_format():
    with pytest.raises(ConfigurationError) as exc:
        rc = InventoryConfig()
        inventories = ['/tmp/inventory1', '/tmp/inventory2']
        rc.prepare_inventory_command('graph', inventories=inventories, response_format='toml')

    assert "'graph' action supports only 'json' response format" == exc.value.args[0]


@pytest.mark.parametrize('runtime', ('docker', 'podman'))
def test_prepare_inventory_command_with_containerization(tmp_path, runtime, mocker):
    mocker.patch.dict('os.environ', {'HOME': str(tmp_path)}, clear=True)
    tmp_path.joinpath('.ssh').mkdir()

    kwargs = {
        'private_data_dir': tmp_path,
        'process_isolation': True,
        'container_image': 'my_container',
        'process_isolation_executable': runtime
    }
    rc = InventoryConfig(**kwargs)
    rc.ident = 'foo'
    inventories = ['/tmp/inventory1', '/tmp/inventory2']
    rc.prepare_inventory_command('list', inventories, response_format='yaml', playbook_dir='/tmp',
                                 vault_ids='1234', vault_password_file='/tmp/password', output_file='/tmp/inv_out.txt',
                                 export=True)

    assert rc.runner_mode == 'subprocess'
    extra_container_args = []
    if runtime == 'podman':
        extra_container_args = ['--quiet']
    else:
        extra_container_args = [f'--user={os.getuid()}']

    expected_command_start = [
        runtime,
        'run',
        '--rm',
        '--interactive',
        '--workdir',
        '/runner/project',
        '-v', f'{rc.private_data_dir}/.ssh/:/home/runner/.ssh/',
        '-v', f'{rc.private_data_dir}/.ssh/:/root/.ssh/',
    ]

    if os.path.exists('/etc/ssh/ssh_known_hosts'):
        expected_command_start.extend(['-v', '/etc/ssh/:/etc/ssh/'])

    if runtime == 'podman':
        expected_command_start.extend(['--group-add=root', '--ipc=host'])

    expected_command_start.extend([
        '-v', f'{rc.private_data_dir}/artifacts/:/runner/artifacts/:Z',
        '-v', f'{rc.private_data_dir}/:/runner/:Z',
        '--env-file', f'{rc.artifact_dir}/env.list',
    ])

    expected_command_start.extend(extra_container_args)

    expected_command_start.extend([
        '--name',
        'distronode_runner_foo',
        'my_container',
        'distronode-inventory',
        '--list',
        '-i', '/tmp/inventory1',
        '-i', '/tmp/inventory2',
        '--yaml',
        '--playbook-dir', '/tmp',
        '--vault-id', '1234',
        '--vault-password-file', '/tmp/password',
        '--output', '/tmp/inv_out.txt',
        '--export',
    ])

    assert expected_command_start == rc.command
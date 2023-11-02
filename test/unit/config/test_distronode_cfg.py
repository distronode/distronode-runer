# -*- coding: utf-8 -*-

import os
import pytest

from distronode_runner.config.distronode_cfg import DistronodeCfgConfig
from distronode_runner.config._base import BaseExecutionMode
from distronode_runner.exceptions import ConfigurationError
from distronode_runner.utils import get_executable_path


def test_distronode_cfg_init_defaults(tmp_path, patch_private_data_dir):
    # pylint: disable=W0613
    rc = DistronodeCfgConfig()

    # Check that the private data dir is placed in our default location with our default prefix
    # and has some extra uniqueness on the end.
    base_private_data_dir = tmp_path.joinpath('.distronode-runner-').as_posix()
    assert rc.private_data_dir.startswith(base_private_data_dir)
    assert len(rc.private_data_dir) > len(base_private_data_dir)

    assert rc.execution_mode == BaseExecutionMode.DISTRONODE_COMMANDS


def test_invalid_runner_mode_value():
    with pytest.raises(ConfigurationError) as exc:
        DistronodeCfgConfig(runner_mode='test')

    assert "Invalid runner mode" in exc.value.args[0]


def test_prepare_config_command():
    rc = DistronodeCfgConfig()
    rc.prepare_distronode_config_command('list', config_file='/tmp/distronode.cfg')
    expected_command = [get_executable_path('distronode-config'), 'list', '-c', '/tmp/distronode.cfg']
    assert rc.command == expected_command
    assert rc.runner_mode == 'subprocess'


def test_prepare_config_invalid_command():
    with pytest.raises(ConfigurationError) as exc:
        rc = DistronodeCfgConfig()
        rc.prepare_distronode_config_command('list', config_file='/tmp/distronode.cfg', only_changed=True)

    assert "only_changed is applicable for action 'dump'" == exc.value.args[0]


def test_prepare_config_invalid_action():
    with pytest.raises(ConfigurationError) as exc:
        rc = DistronodeCfgConfig()
        rc.prepare_distronode_config_command('test')

    assert "Invalid action test, valid value is one of either list, dump, view" == exc.value.args[0]


@pytest.mark.parametrize('runtime', ('docker', 'podman'))
def test_prepare_config_command_with_containerization(tmp_path, runtime, mocker):
    mocker.patch.dict('os.environ', {'HOME': str(tmp_path)}, clear=True)
    tmp_path.joinpath('.ssh').mkdir()

    kwargs = {
        'private_data_dir': tmp_path,
        'process_isolation': True,
        'container_image': 'my_container',
        'process_isolation_executable': runtime
    }
    rc = DistronodeCfgConfig(**kwargs)
    rc.ident = 'foo'
    rc.prepare_distronode_config_command('list', config_file='/tmp/distronode.cfg')

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
        '-v', f'{str(tmp_path)}/.ssh/:/root/.ssh/',
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
        'distronode-config',
        'list',
        '-c',
        '/tmp/distronode.cfg',
    ])

    assert expected_command_start == rc.command

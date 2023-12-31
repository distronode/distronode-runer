############################
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

# pylint: disable=W0201

import logging

from distronode_runner.config._base import BaseConfig, BaseExecutionMode
from distronode_runner.exceptions import ConfigurationError
from distronode_runner.utils import get_executable_path

logger = logging.getLogger('distronode-runner')


class DocConfig(BaseConfig):
    """
    A ``Runner`` configuration object that's meant to encapsulate the configuration used by the
    :py:mod:`distronode_runner.runner.DocConfig` object to launch and manage the invocation of
    command execution.

    Typically this object is initialized for you when using the standard ``get_plugin_docs`` or ``get_plugin_list`` interfaces
    in :py:mod:`distronode_runner.interface` but can be used to construct the ``DocConfig`` configuration to be invoked elsewhere.
    It can also be overridden to provide different functionality to the DocConfig object.

    :Example:

    >>> dc = DocConfig(...)
    >>> r = Runner(config=dc)
    >>> r.run()

    """

    def __init__(self, runner_mode=None, **kwargs):
        # runner params
        self.runner_mode = runner_mode if runner_mode else 'subprocess'
        if self.runner_mode not in ['pexpect', 'subprocess']:
            raise ConfigurationError(f"Invalid runner mode {self.runner_mode}, valid value is either 'pexpect' or 'subprocess'")

        if kwargs.get("process_isolation"):
            self._distronode_doc_exec_path = "distronode-doc"
        else:
            self._distronode_doc_exec_path = get_executable_path("distronode-doc")

        self.execution_mode = BaseExecutionMode.DISTRONODE_COMMANDS
        super().__init__(**kwargs)

    _supported_response_formats = ('json', 'human')

    def prepare_plugin_docs_command(self, plugin_names, plugin_type=None, response_format=None,
                                    snippet=False, playbook_dir=None, module_path=None):

        if response_format and response_format not in DocConfig._supported_response_formats:
            raise ConfigurationError(f'Invalid response_format {response_format}, '
                                     f'valid value is one of either {", ".join(DocConfig._supported_response_formats)}')

        if not isinstance(plugin_names, list):
            raise ConfigurationError(f"plugin_names should be of type list, instead received {plugin_names} of type {type(plugin_names)}")

        self.prepare_env(runner_mode=self.runner_mode)
        self.cmdline_args = []

        if response_format == 'json':
            self.cmdline_args.append('-j')

        if snippet:
            self.cmdline_args.append('-s')

        if plugin_type:
            self.cmdline_args.extend(['-t', plugin_type])

        if playbook_dir:
            self.cmdline_args.extend(['--playbook-dir', playbook_dir])

        if module_path:
            self.cmdline_args.extend(['-M', module_path])

        self.cmdline_args.extend(plugin_names)

        self.command = [self._distronode_doc_exec_path] + self.cmdline_args
        self.handle_command_wrap(self.execution_mode, self.cmdline_args)

    def prepare_plugin_list_command(self, list_files=None, response_format=None, plugin_type=None,
                                    playbook_dir=None, module_path=None):

        if response_format and response_format not in DocConfig._supported_response_formats:
            raise ConfigurationError(f"Invalid response_format {response_format}, "
                                     f'valid value is one of either {", ".join(DocConfig._supported_response_formats)}')

        self.prepare_env(runner_mode=self.runner_mode)
        self.cmdline_args = []

        if list_files:
            self.cmdline_args.append('-F')
        else:
            self.cmdline_args.append('-l')

        if response_format == 'json':
            self.cmdline_args.append('-j')

        if plugin_type:
            self.cmdline_args.extend(['-t', plugin_type])

        if playbook_dir:
            self.cmdline_args.extend(['--playbook-dir', playbook_dir])

        if module_path:
            self.cmdline_args.extend(['-M', module_path])

        self.command = [self._distronode_doc_exec_path] + self.cmdline_args
        self.handle_command_wrap(self.execution_mode, self.cmdline_args)

    def prepare_role_list_command(self, collection_name, playbook_dir):
        """
        distronode-doc -t role -l -j <collection_name>
        """
        self.prepare_env(runner_mode=self.runner_mode)
        self.cmdline_args = ['-t', 'role', '-l', '-j']
        if playbook_dir:
            self.cmdline_args.extend(['--playbook-dir', playbook_dir])
        if collection_name:
            self.cmdline_args.append(collection_name)

        self.command = [self._distronode_doc_exec_path] + self.cmdline_args
        self.handle_command_wrap(self.execution_mode, self.cmdline_args)

    def prepare_role_argspec_command(self, role_name, collection_name, playbook_dir):
        """
        distronode-doc -t role -j <collection_name>.<role_name>
        """
        self.prepare_env(runner_mode=self.runner_mode)
        self.cmdline_args = ['-t', 'role', '-j']
        if playbook_dir:
            self.cmdline_args.extend(['--playbook-dir', playbook_dir])
        if collection_name:
            role_name = ".".join([collection_name, role_name])
        self.cmdline_args.append(role_name)

        self.command = [self._distronode_doc_exec_path] + self.cmdline_args
        self.handle_command_wrap(self.execution_mode, self.cmdline_args)

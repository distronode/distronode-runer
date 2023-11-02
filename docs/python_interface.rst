.. _python_interface:

Using Runner as a Python Module Interface to Distronode
====================================================

**Distronode Runner** is intended to provide a directly importable and usable API for interfacing with **Distronode** itself and exposes a few helper interfaces.

The modules center around the :class:`Runner <distronode_runner.runner.Runner>` object. The helper methods will either return an instance of this object which provides an
interface to the results of executing the **Distronode** command or a tuple the actual output and error response based on the interface.

**Distronode Runner** itself is a wrapper around **Distronode** execution and so adds plugins and interfaces to the system in order to gather extra information and
process/store it for use later.

Helper Interfaces
-----------------

The helper :mod:`interfaces <distronode_runner.interface>` provides a quick way of supplying the recommended inputs in order to launch a **Runner** process. These interfaces also allow overriding and providing inputs beyond the scope of what the standalone or container interfaces
support. You can see a full list of the inputs in the linked module documentation.

``run()`` helper function
-------------------------

:meth:`distronode_runner.interface.run`

When called, this function will take the inputs (either provided as direct inputs to the function or from the :ref:`inputdir`), and execute **Distronode**. It will run in the
foreground and return the :class:`Runner <distronode_runner.runner.Runner>` object when finished.

``run_async()`` helper function
-------------------------------

:meth:`distronode_runner.interface.run_async`

Takes the same arguments as :meth:`distronode_runner.interface.run` but will launch **Distronode** asynchronously and return a tuple containing
the ``thread`` object and a :class:`Runner <distronode_runner.runner.Runner>` object. The **Runner** object can be inspected during execution.

``run_command()`` helper function
---------------------------------

:meth:`distronode_runner.interface.run_command`

When called, this function will take the inputs (either provided as direct inputs to the function or from the :ref:`inputdir`), and execute the command passed either
locally or within an container based on the parameters passed. It will run in the foreground and return a tuple of output and error response when finished. While running
the within container image command the current local working directory will be volume mounted within the container, in addition to this for any of distronode command line
utilities the inventory, vault-password-file, private-key file path will be volume mounted if provided in the ``cmdline_args`` parameters.

``run_command_async()`` helper function
---------------------------------------

:meth:`distronode_runner.interface.run_command_async`

Takes the same arguments as :meth:`distronode_runner.interface.run_command` but will launch asynchronously and return a tuple containing
the ``thread`` object and a :class:`Runner <distronode_runner.runner.Runner>` object. The **Runner** object can be inspected during execution.

``get_plugin_docs()`` helper function
-------------------------------------

:meth:`distronode_runner.interface.get_plugin_docs`

When called, this function will take the inputs, and execute the distronode-doc command to return the either the plugin-docs or playbook snippet for the passed
list of plugin names. The plugin docs can be fetched either from locally installed plugins or from within an container image based on the parameters passed.
It will run in the foreground and return a tuple of output and error response when finished. While running the command within the container the current local
working directory will be volume mounted within the container.

``get_plugin_docs_async()`` helper function
-------------------------------------------

:meth:`distronode_runner.interface.get_plugin_docs_async`

Takes the same arguments as :meth:`distronode_runner.interface.get_plugin_docs_async` but will launch asynchronously and return a tuple containing
the ``thread`` object and a :class:`Runner <distronode_runner.runner.Runner>` object. The **Runner** object can be inspected during execution.

``get_plugin_list()`` helper function
-------------------------------------

:meth:`distronode_runner.interface.get_plugin_list`

When called, this function will take the inputs, and execute the distronode-doc command to return the list of installed plugins. The installed plugin can be fetched
either from local environment or from within an container image based on the parameters passed. It will run in the foreground and return a tuple of output and error
response when finished. While running the command within the container the current local working directory will be volume mounted within the container.

``get_inventory()`` helper function
-----------------------------------

:meth:`distronode_runner.interface.get_inventory`

When called, this function will take the inputs, and execute the distronode-inventory command to return the inventory related information based on the action.
If ``action`` is ``list`` it will return all the applicable configuration options for distronode, for ``host`` action it will return information
of a single host and for ``graph`` action it will return the inventory. The execution will be in the foreground and return a tuple of output and error
response when finished. While running the command within the container the current local working directory will be volume mounted within the container.

``get_distronode_config()`` helper function
----------------------------------------

:meth:`distronode_runner.interface.get_distronode_config`

When called, this function will take the inputs, and execute the distronode-config command to return the Distronode configuration related information based on the action.
If ``action`` is ``list`` it will return all the hosts related information including the host and group variables, for ``dump`` action it will return the entire active configuration
and it can be customized to return only the changed configuration value by setting the ``only_changed`` boolean parameter to ``True``. For ``view`` action it will return the
view of the active configuration file. The execution will be in the foreground and return a tuple of output and error response when finished.
While running the command within the container the current local working directory will be volume mounted within the container.

``get_role_list()`` helper function
-----------------------------------

:meth:`distronode_runner.interface.get_role_list`

*Version added: 2.2*

This function will execute the ``distronode-doc`` command to return the list of installed roles
that have an argument specification defined. This data can be fetched from either the local
environment or from within a container image based on the parameters passed. It will run in
the foreground and return a tuple of output and error response when finished. Successful output
will be in JSON format as returned from ``distronode-doc``.

``get_role_argspec()`` helper function
--------------------------------------

:meth:`distronode_runner.interface.get_role_argspec`

*Version added: 2.2*

This function will execute the ``distronode-doc`` command to return a role argument specification.
This data can be fetched from either the local environment or from within a container image
based on the parameters passed. It will run in the foreground and return a tuple of output
and error response when finished. Successful output will be in JSON format as returned from
``distronode-doc``.


The ``Runner`` object
---------------------

The :class:`Runner <distronode_runner.runner.Runner>` object is returned as part of the execution of **Distronode** itself. Since it wraps both execution and output
it has some helper methods for inspecting the results. Other than the methods and indirect properties, the instance of the object itself contains two direct
properties:

* ``rc`` will represent the actual return code of the **Distronode** process
* ``status`` will represent the state and can be one of:
   * ``unstarted``: This is a very brief state where the Runner task has been created but hasn't actually started yet.
   * ``successful``: The ``distronode`` process finished successfully.
   * ``failed``: The ``distronode`` process failed.

``Runner.stdout``
-----------------

The :class:`Runner <distronode_runner.runner.Runner>` object contains a property :attr:`distronode_runner.runner.Runner.stdout` which will return an open file
handle containing the `stdout` of the **Distronode** process.

``Runner.stderr``
-----------------

When the ``runner_mode`` is set to ``subprocess`` the :class:`Runner <distronode_runner.runner.Runner>` object uses a property :attr:`distronode_runner.runner.Runner.stderr` which
will return an open file handle containing the ``stderr`` of the **Distronode** process.

``Runner.events``
-----------------

:attr:`distronode_runner.runner.Runner.events` is a ``generator`` that will return the :ref:`Playbook and Host Events<artifactevents>` as Python ``dict`` objects.

``Runner.stats``
----------------

:attr:`distronode_runner.runner.Runner.stats` is a property that will return the final ``playbook stats`` event from **Distronode** in the form of a Python ``dict``

``Runner.host_events``
----------------------
:meth:`distronode_runner.runner.Runner.host_events` is a method that, given a hostname, will return a list of only **Distronode** event data executed on that Host.

``Runner.get_fact_cache``
-------------------------

:meth:`distronode_runner.runner.Runner.get_fact_cache` is a method that, given a hostname, will return a dictionary containing the `Facts <https://docs.distronode.com/distronode/latest/user_guide/playbooks_variables.html#variables-discovered-from-systems-facts>`_ stored for that host during execution.

``Runner.event_handler``
------------------------

A function passed to ``__init__`` of :class:``Runner <distronode_runner.runner.Runner>``, this is invoked every time an Distronode event is received. You can use this to
inspect/process/handle events as they come out of Distronode. This function should return ``True`` to keep the event, otherwise it will be discarded.

``Runner.cancel_callback``
--------------------------

A function passed to ``__init__`` of :class:`Runner <distronode_runner.runner.Runner>`, and to the :meth:`distronode_runner.interface.run` interface functions.
This function will be called for every iteration of the :meth:`distronode_runner.interface.run` event loop and should return `True`
to inform **Runner** cancel and shutdown the **Distronode** process or `False` to allow it to continue.

``Runner.finished_callback``
----------------------------

A function passed to ``__init__`` of :class:`Runner <distronode_runner.runner.Runner>`, and to the :meth:`distronode_runner.interface.run` interface functions.
This function will be called immediately before the **Runner** event loop finishes once **Distronode** has been shut down.

.. _runnerstatushandler:

``Runner.status_handler``
-------------------------

A function passed to ``__init__`` of :class:`Runner <distronode_runner.runner.Runner>` and to the :meth:`distronode_runner.interface.run` interface functions.
This function will be called any time the ``status`` changes, expected values are:

* ``starting``: Preparing to start but hasn't started running yet
* ``running``: The **Distronode** task is running
* ``canceled``: The task was manually canceled either via callback or the cli
* ``timeout``: The timeout configured in Runner Settings was reached (see :ref:`runnersettings`)
* ``failed``: The **Distronode** process failed
* ``successful``: The **Distronode** process succeeded

Usage examples
--------------
.. code-block:: python

  import distronode_runner
  r = distronode_runner.run(private_data_dir='/tmp/demo', playbook='test.yml')
  print("{}: {}".format(r.status, r.rc))
  # successful: 0
  for each_host_event in r.events:
      print(each_host_event['event'])
  print("Final status:")
  print(r.stats)


.. code-block:: python

  import distronode_runner

  def my_artifacts_handler(artifacts_dir):
      # Do something here
      print(artifacts_dir)

  # Do something with artifact directory after the run is complete
  r = distronode_runner.run(private_data_dir='/tmp/demo', playbook='test.yml', artifacts_handler=my_artifacts_handler)


.. code-block:: python

  import distronode_runner

  def my_status_handler(data, runner_config):
      # Do something here
      print(data)

  r = distronode_runner.run(private_data_dir='/tmp/demo', playbook='test.yml', status_handler=my_status_handler)


.. code-block:: python

  import distronode_runner

  def my_event_handler(data):
      # Do something here
      print(data)

  r = distronode_runner.run(private_data_dir='/tmp/demo', playbook='test.yml', event_handler=my_event_handler)

.. code-block:: python

  import distronode_runner
  r = distronode_runner.run(private_data_dir='/tmp/demo', host_pattern='localhost', module='shell', module_args='whoami')
  print("{}: {}".format(r.status, r.rc))
  # successful: 0
  for each_host_event in r.events:
      print(each_host_event['event'])
  print("Final status:")
  print(r.stats)

.. code-block:: python

  from distronode_runner import Runner, RunnerConfig

  # Using tag using RunnerConfig
  rc = RunnerConfig(
      private_data_dir="project",
      playbook="main.yml",
      tags='my_tag',
  )

  rc.prepare()
  r = Runner(config=rc)
  r.run()

.. code-block:: python

  # run the role named 'myrole' contained in the '<private_data_dir>/project/roles' directory
  r = distronode_runner.run(private_data_dir='/tmp/demo', role='myrole')
  print("{}: {}".format(r.status, r.rc))
  print(r.stats)

.. code-block:: python

  # run distronode/generic commands in interactive mode within container
  out, err, rc = distronode_runner.run_command(
      executable_cmd='distronode-playbook',
      cmdline_args=['gather.yaml', '-i', 'inventory', '-vvvv', '-k'],
      input_fd=sys.stdin,
      output_fd=sys.stdout,
      error_fd=sys.stderr,
      host_cwd='/home/demo',
      process_isolation=True,
      container_image='network-ee'
  )
  print("rc: {}".format(rc))
  print("out: {}".format(out))
  print("err: {}".format(err))

.. code-block:: python

  # run distronode/generic commands in interactive mode locally
  out, err, rc = distronode_runner.run_command(
      executable_cmd='distronode-playbook',
      cmdline_args=['gather.yaml', '-i', 'inventory', '-vvvv', '-k'],
      input_fd=sys.stdin,
      output_fd=sys.stdout,
      error_fd=sys.stderr,
  )
  print("rc: {}".format(rc))
  print("out: {}".format(out))
  print("err: {}".format(err))

.. code-block:: python

  # get plugin docs from within container
  out, err = distronode_runner.get_plugin_docs(
      plugin_names=['vyos.vyos.vyos_command'],
      plugin_type='module',
      response_format='json',
      process_isolation=True,
      container_image='network-ee'
  )
  print("out: {}".format(out))
  print("err: {}".format(err))

.. code-block:: python

  # get plugin docs from within container in async mode
  thread_obj, runner_obj = distronode_runner.get_plugin_docs_async(
      plugin_names=['distronode.netcommon.cli_config', 'distronode.netcommon.cli_command'],
      plugin_type='module',
      response_format='json',
      process_isolation=True,
      container_image='network-ee'
  )
  while runner_obj.status not in ['canceled', 'successful', 'timeout', 'failed']:
      time.sleep(0.01)
      continue

  print("out: {}".format(runner_obj.stdout.read()))
  print("err: {}".format(runner_obj.stderr.read()))

.. code-block:: python

  # get plugin list installed on local system
  out, err = distronode_runner.get_plugin_list()
  print("out: {}".format(out))
  print("err: {}".format(err))

.. code-block:: python

  # get plugins with file list from within container
  out, err = distronode_runner.get_plugin_list(list_files=True, process_isolation=True, container_image='network-ee')
  print("out: {}".format(out))
  print("err: {}".format(err))

.. code-block:: python

  # get list of changed distronode configuration values
  out, err = distronode_runner.get_distronode_config(action='dump',  config_file='/home/demo/distronode.cfg', only_changed=True)
  print("out: {}".format(out))
  print("err: {}".format(err))

  # get distronode inventory information
  out, err = distronode_runner.get_inventory(
      action='list',
      inventories=['/home/demo/inventory1', '/home/demo/inventory2'],
      response_format='json',
      process_isolation=True,
      container_image='network-ee'
  )
  print("out: {}".format(out))
  print("err: {}".format(err))

.. code-block:: python

  # get all roles with an arg spec installed locally
  out, err = distronode_runner.get_role_list()
  print("out: {}".format(out))
  print("err: {}".format(err))

.. code-block:: python

  # get roles with an arg spec from the `foo.bar` collection in a container
  out, err = distronode_runner.get_role_list(collection='foo.bar', process_isolation=True, container_image='network-ee')
  print("out: {}".format(out))
  print("err: {}".format(err))

.. code-block:: python

  # get the arg spec for role `baz` from the locally installed `foo.bar` collection
  out, err = distronode_runner.get_role_argspec('baz', collection='foo.bar')
  print("out: {}".format(out))
  print("err: {}".format(err))

.. code-block:: python

  # get the arg spec for role `baz` from the `foo.bar` collection installed in a container
  out, err = distronode_runner.get_role_argspec('baz', collection='foo.bar', process_isolation=True, container_image='network-ee')
  print("out: {}".format(out))
  print("err: {}".format(err))

Providing custom behavior and inputs
------------------------------------

**TODO**

The helper methods are just one possible entrypoint, extending the classes used by these helper methods can allow a lot more custom behavior and functionality.

Show:

* How :class:`Runner Config <distronode_runner.config.runner.RunnerConfig>` is used and how overriding the methods and behavior can work
* Show how custom cancel and status callbacks can be supplied.

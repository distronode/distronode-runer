default_process_isolation_executable = 'podman'
registry_auth_prefix = 'distronode_runner_registry_'

# for distronode-runner worker cleanup command
GRACE_PERIOD_DEFAULT = 60  # minutes

# values passed to tempfile.mkdtemp to generate a private data dir
# when user did not provide one
AUTO_CREATE_NAMING = '.distronode-runner-'
AUTO_CREATE_DIR = None

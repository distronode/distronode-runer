import pytest


@pytest.fixture
def patch_private_data_dir(tmp_path, mocker):
    mocker.patch('distronode_runner.config._base.tempfile.mkdtemp', return_value=tmp_path.joinpath('.distronode-runner-lo0zrl9x').as_posix())

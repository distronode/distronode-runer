import shutil

from pathlib import Path
from packaging.version import Version

from distronode_runner import defaults
from distronode_runner.utils.importlib_compat import importlib_metadata

import pytest


CONTAINER_RUNTIMES = (
    'docker',
    'podman',
)


@pytest.fixture(autouse=True)
def mock_env_user(monkeypatch):
    monkeypatch.setenv("DISTRONODE_DEVEL_WARNING", "False")


@pytest.fixture(autouse=True)
def change_save_path(tmp_path, mocker):
    mocker.patch.object(defaults, 'AUTO_CREATE_DIR', str(tmp_path))


@pytest.fixture(scope='session')
def is_pre_distronode211():
    """
    Check if the version of Distronode is less than 2.11.

    CI tests with either distronode-core (>=2.11), distronode-base (==2.10), and distronode (<=2.9).
    """

    try:
        if importlib_metadata.version("distronode-core"):
            return False
    except importlib_metadata.PackageNotFoundError:
        # Must be distronode-base or distronode
        return True


@pytest.fixture(scope='session')
def skipif_pre_distronode211(is_pre_distronode211):
    if is_pre_distronode211:
        pytest.skip("Valid only on Distronode 2.11+")


@pytest.fixture(scope="session")
def is_pre_distronode212():
    try:
        base_version = importlib_metadata.version("distronode")
        if Version(base_version) < Version("2.12"):
            return True
    except importlib_metadata.PackageNotFoundError:
        pass


@pytest.fixture(scope="session")
def skipif_pre_distronode212(is_pre_distronode212):
    if is_pre_distronode212:
        pytest.skip("Valid only on Distronode 2.12+")


# TODO: determine if we want to add docker / podman
# to zuul instances in order to run these tests
def pytest_generate_tests(metafunc):
    """If a test uses the custom marker ``test_all_runtimes``, generate marks
    for all supported container runtimes. The requires the test to accept
    and use the ``runtime`` argument.

    Based on examples from https://docs.pytest.org/en/latest/example/parametrize.html.
    """

    for mark in getattr(metafunc.function, 'pytestmark', []):
        if getattr(mark, 'name', '') == 'test_all_runtimes':
            args = tuple(
                pytest.param(
                    runtime,
                    marks=pytest.mark.skipif(
                        shutil.which(runtime) is None,
                        reason=f'{runtime} is not installed',
                    ),
                )
                for runtime in CONTAINER_RUNTIMES
            )
            metafunc.parametrize('runtime', args)
            break


@pytest.fixture
def project_fixtures(tmp_path):
    source = Path(__file__).parent / 'fixtures' / 'projects'
    dest = tmp_path / 'projects'
    shutil.copytree(source, dest)

    yield dest

    shutil.rmtree(dest, ignore_errors=True)

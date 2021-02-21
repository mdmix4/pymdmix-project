import yaml
import json
import os
import pytest

from pymdmix_core.orm import SQL_SESSION
from pymdmix_project.project import Project
from .conftest import run_command


# TODO:
# test projects can be deleted in bulk keeping and deleting the project folders


@pytest.mark.parametrize("format,dump", [("yaml", yaml.dump), ("json", json.dump)])
def test_project_create_from_file(format, dump, tmpdir):
    """
    Test:
        project creation, one by one, from yaml/json config files.
        project deletion, one by one, removing the folder
    """
    name = "test_project"
    path = os.path.join(tmpdir, name)
    fields = {
        "id": name,
        "description": "test_project description",
        "path": path
    }
    filename = os.path.join(tmpdir, f"{name}.{format}")
    with open(filename, 'w') as f:
        dump(fields, f)

    run_command(command=["project", "create", f"--{format}", filename])
    assert os.path.exists(path)
    assert len(SQL_SESSION.query(Project).all()) == 1
    run_command(command=["project", "delete", "--remove-data", name])
    assert os.path.exists(path) is False
    assert len(SQL_SESSION.query(Project).all()) == 0


def test_project_create_from_arguments(tmpdir):
    """
    Test:
        project creation from arguments, with path
        project deletion keeping files
    """
    name = "test_project"
    path = os.path.join(tmpdir, name)
    run_command(command=["project", "create", "--name", name, "--path", path])
    assert os.path.exists(path)
    assert len(SQL_SESSION.query(Project).all()) == 1
    run_command(command=["project", "delete", name])
    assert os.path.exists(path)
    assert len(SQL_SESSION.query(Project).all()) == 0


@pytest.mark.parametrize(
    "remove_data", [
        pytest.param(True, id="Remove data"),
        pytest.param(False, id="Keep data")
    ]
)
def test_project_create_with_implicit_path(remove_data, tmpdir):
    """
    Test:
        project creation with implicit path
        project deletion in bulk, keeping and deleting files
    """
    cwd = os.getcwd()
    os.chdir(tmpdir)
    names = ["test_project1", "test_project2"]
    for name in names:
        run_command(command=["project", "create", "--name", name])
        assert os.path.exists(name)
    assert len(SQL_SESSION.query(Project).all()) == 2
    delete_command = ["project", "delete"]
    if remove_data:
        delete_command.append("--remove-data")
    delete_command += names
    run_command(command=delete_command)
    for name in names:
        assert os.path.exists(name) != remove_data
    assert len(SQL_SESSION.query(Project).all()) == 0
    os.chdir(cwd)

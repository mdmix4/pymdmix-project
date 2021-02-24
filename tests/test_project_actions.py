import yaml
import json
import os
import pytest

from pymdmix_project.project import Project, ProjectPlugin
from .conftest import run_command, get_plugin_manager, db_patch


@db_patch()
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
    plugin_manager = get_plugin_manager()
    plugin: ProjectPlugin = plugin_manager.plugins["project"]
    session = plugin.session

    run_command(f"project create --{format} {filename}", plugin_manager)
    assert os.path.exists(path)
    assert len(session.query(Project).all()) == 1

    run_command(f"project delete --remove-data {name}", plugin_manager)
    assert os.path.exists(path) is False
    assert len(session.query(Project).all()) == 0


@db_patch()
def test_project_create_from_arguments(tmpdir):
    """
    Test:
        project creation from arguments, with path
        project deletion keeping files
    """
    name = "test_project"
    path = os.path.join(tmpdir, name)
    plugin_manager = get_plugin_manager()
    plugin: ProjectPlugin = plugin_manager.plugins["project"]
    session = plugin.session

    run_command(f"project create --name {name} --path {path}", plugin_manager)
    assert os.path.exists(path)
    assert len(session.query(Project).all()) == 1

    run_command(f"project delete {name}", plugin_manager)
    assert os.path.exists(path)
    assert len(session.query(Project).all()) == 0


@db_patch()
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
    plugin_manager = get_plugin_manager()
    plugin: ProjectPlugin = plugin_manager.plugins["project"]
    session = plugin.session

    for name in names:
        run_command(f"project create --name {name}", plugin_manager)
        assert os.path.exists(name)
    assert len(session.query(Project).all()) == 2

    delete_command = ["project delete"]
    if remove_data:
        delete_command.append("--remove-data")
    delete_command += names
    run_command(" ".join(delete_command), plugin_manager)
    for name in names:
        assert os.path.exists(name) != remove_data
    assert len(session.query(Project).all()) == 0
    os.chdir(cwd)

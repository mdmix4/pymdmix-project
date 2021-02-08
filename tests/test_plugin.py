from pymdmix_core.plugin import PluginManager


def test_plugin_manager_load_plugin():
    plugin_manager = PluginManager()
    plugin_manager.load_plugin("pymdmix_project")

    assert "project" in plugin_manager.plugins

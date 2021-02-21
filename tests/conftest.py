from typing import List
from pymdmix_core.parser import get_mdmix_parser
from pymdmix_core.plugin.base import PluginManager


def get_plugin_manager():
    plugin_manager = PluginManager(get_mdmix_parser())
    plugin_manager.load_plugin("pymdmix_project")
    return plugin_manager


def run_command(command: List[str], plugin_manager: PluginManager = None):
    plugin_manager = plugin_manager if plugin_manager is not None else get_plugin_manager()
    args = plugin_manager.parser.parse_args(command)
    plugin_manager.plugins["project"].run(args)

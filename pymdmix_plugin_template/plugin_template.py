from pymdmix_core.plugin import Plugin


class PluginTemplate(Plugin):

    NAME = "plugin_template"

    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        pass

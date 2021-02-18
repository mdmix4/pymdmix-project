from argparse import Namespace
from sqlalchemy import Column, String
from pymdmix_core.orm import BaseModel
from pymdmix_core.plugin.crud import CRUDPlugin
from pymdmix_core.plugin.crud import ActionCreate



class ActionCreateProject(ActionCreate):

    def init_parser(self):
        super().init_parser()
        self.parser.add_argument("--name", "-n")
        self.parser.add_argument("--path", "-p")
        self.parser.add_argument("--description", "-d")

    def run(self, args: Namespace):
        # create the project dir and if it work fine, then put it in the database
        super().run(args)


class Project(BaseModel):
    __tablename__ = "projects"
    id = Column(String(128), unique=True, primary_key=True)
    description = Column(String(1024))
    path = Column(String(256))

    def __repr__(self):
        return f"Project: {self.id} @ {self.path}"


class ProjectPlugin(CRUDPlugin):

    NAME = "project"
    CLASS = Project

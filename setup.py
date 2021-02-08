#!/usr/bin/env python3

from setuptools import setup


def getRequirements():
    requirements = []
    with open("requirements.txt", "r") as reqfile:
        for line in reqfile.readlines():
            requirements.append(line.strip())
    return requirements


def getVersion():
    return "0.0.1"


setup(
    python_requires=">=3.8",
    name="pymdmix-plugin-template",
    version=getVersion(),
    description="Plugin template for kick-starting a new project",
    author="ggutierrez-bio",
    author_email="",
    url="https://github.com/ggutierrez-bio/mdmix4",
    data_files=[("pymdmix", ["defaults/pymdmix_plugin_template.yml"])],
    packages=["pymdmix_plugin_template"],
    install_requires=getRequirements(),
)

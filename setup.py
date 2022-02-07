import pathlib

import pkg_resources
from setuptools import setup, find_packages

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name='pypeline',
    version='0.0.0',
    setup_requires=['wheel'],
    packages=[*find_packages()],
    requires=[*install_requires],

    description='generic lazy execution',
    author='Yuval Gershon',
    author_email='yuvalgershon101@gmail.com',
    url='https://github.com/TentacleHorn/Pypeline',

)

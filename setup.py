from setuptools import setup
from mpilot import __version__ as version

setup(
    name="mpilot",
    description="MPilot is a plugin-based, environmental modeling framework",
    keywords="mpilot,eems",
    version=version,
    packages=["mpilot", "mpilot.cli", "mpilot.parser"],
    install_requires=["ply", "six", "click", "numpy", "netcdf4"],
    entry_points={"console_scripts": ["mpilot=mpilot.cli.mpilot:main"]},
)

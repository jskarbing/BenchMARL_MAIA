#  Copyright (c) Meta Platforms, Inc. and affiliates.
#
#  This source code is licensed under the license found in the
#  LICENSE file in the root directory of this source tree.
#
import os
import pathlib
from pathlib import Path

from setuptools import find_packages, setup


def package_files(directory):
    paths = []
    for path, _, filenames in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


def get_version():
    """Gets the benchmarl version."""
    path = CWD / "benchmarl" / "__init__.py"
    content = path.read_text()

    for line in content.splitlines():
        if line.startswith("__version__"):
            return line.strip().split()[-1].strip().strip('"')
    raise RuntimeError("bad version data in __init__.py")


CWD = pathlib.Path(__file__).absolute().parent

extra_files = package_files(
    str(
        Path(os.path.dirname(os.path.realpath(__file__)))
        / Path("benchmarl")
        / Path("conf")
    )
)

setup(
    name="benchmarl_maia",
    version=get_version(),
    description="BenchMARL MAIA",
    url="https://github.com/jskarbing/BenchMARL_MAIA/",
    author="Original BenchMARL: Matteo Bettini, MAIA modifications: Julia Karbing",
    author_email="Original BenchMARL: mb2389@cl.cam.ac.uk, MAIA modifications: julia.karbing@robots.ox.ac.uk",
    install_requires=["torchrl~=0.8.0", "tqdm", "hydra-core", "torchvision", "av<14"],
    extras_require={
        "vmas": ["vmas>=1.3.4"],
        "pettingzoo": ["pettingzoo[all]>=1.24.3"],
        "meltingpot": ["dm-meltingpot"],
        "gnn": ["torch_geometric"],
        "logging": ["moviepy", "wandb"],
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={"": extra_files},
)

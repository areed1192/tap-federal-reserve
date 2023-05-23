#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-federal-reserve",
    version="0.1.0",
    description="Singer.io tap for extracting data from the United States Federal Reserve.",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_federal_reserve"],
    install_requires=[
        "singer-python==5.12.1",
        "requests==2.31.0",
    ],
    entry_points="""
    [console_scripts]
    tap-federal-reserve=tap_federal_reserve:main
    """,
    packages=["tap_federal_reserve"],
    package_data={
        "schemas": ["tap_federal_reserve/schemas/*.json"]
    },
    include_package_data=True,
)

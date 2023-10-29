#!/usr/bin/env python

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weBGP",
    version="0.0",
    author="Mohsen Tahmasebi",
    author_email="moh53n@outlook.com",
    description="BGP insight tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moh53n/weBGP",
    project_urls={
        "Bug Tracker": "https://github.com/moh53n/weBGP/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    license='MIT',
    install_requires=['websockets', 'iso3166', 'requests'],
    entry_points={
    'console_scripts': [
        'weBGP = src.core.console:main',
    ],},
)

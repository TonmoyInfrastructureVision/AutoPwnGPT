#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# Read version from version.py
version = {}
with open(os.path.join("src", "version.py")) as f:
    exec(f.read(), version)

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    # Skip comments and empty lines
    requirements = [
        line.strip() for line in f
        if line.strip() and not line.startswith("#") and not line.startswith("# ")
    ]

setup(
    name="autopwngpt",
    version=version.get("__version__", "0.1.0"),
    author="Eshan Roy",
    author_email="m.eshanized@gmail.com",
    description="Natural language-powered penetration testing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TonmoyInfrastructureVision/AutoPwnGPT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "autopwngpt=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "autopwngpt": ["data/*", "data/templates/*", "data/wordlists/*"],
    },
)

#  Copyright (c) SecretBiology  2020.
#
#  Library Name: SecretColors
#  Author: Rohit Suratekar
#  Website: https://github.com/secretBiology/SecretColors
#

import setuptools

with open("PYPI.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SecretColors",
    version="1.2.0",
    author="Rohit Suratekar",
    author_email="rohitsuratekar@gmail.com",
    description="A small package for fantastic color palette",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/secretBiology/SecretColors",
    packages=setuptools.find_packages(),
    license='MIT License',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

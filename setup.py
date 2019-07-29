import setuptools

with open("PYPI.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SecretColors",
    version="1.1.0",
    author="Rohit Suratekar",
    author_email="rohitsuratekar@gmail.com",
    description="A small package for fantastic color palette",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/secretBiology/SecretColors",
    packages=setuptools.find_packages(),
    license='MIT License',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

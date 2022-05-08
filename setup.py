import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh.readlines()]

setuptools.setup(
    name="avrae-automation-common",
    version="3.6.9",
    author="Andrew Zhu",
    author_email="andrew@zhu.codes",
    description="Common automation utilities for Avrae",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avrae/automation-common",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)

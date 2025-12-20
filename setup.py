from setuptools import setup, find_packages

setup(
    name="encrypted-journal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cryptography",
    ],
    entry_points={
        "console_scripts": [
            "journal=journal.cli:main",
        ],
    },
)

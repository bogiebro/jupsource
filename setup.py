from setuptools import setup, find_packages

setup(
    name='jupsource',
    version='0.1',
    packages=find_packages(),
    package_data={"jupsource": ["*.jq"]},
    install_requires=["pyjq", "nbformat"]
)

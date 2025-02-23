from setuptools import setup, find_packages

setup(
    name="flask-calculator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "pytest",
    ],
) 
# setup.py
from setuptools import setup, find_packages

setup(
    name="gestion_transacciones_hsa",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pymongo',
    ],
)
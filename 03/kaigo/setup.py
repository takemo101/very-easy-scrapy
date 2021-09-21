# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='kaigo',
    version='1.0',
    packages=find_packages(),
    package_data={},
    entry_points={'scrapy': ['settings = kaigo.settings']},
    zip_safe=False,
)

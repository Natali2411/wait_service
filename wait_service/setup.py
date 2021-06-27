
from distutils.core import setup
from setuptools import find_packages

setup(
    name='wait_service',
    packages=find_packages(exclude=['test', '*.test', '*.test.*']),
    version='1.0',
    description='Wait service',
    author='Nataliia Tiutiunnyk',
    author_email='ntiutiunnyk@b2bsoft.com',
    url='https://github.com/Natali2411/wait_service',
    download_url='https://github.com/Natali2411/wait_service/archive/1.0.tar.gz',
    keywords=['math'],
    scripts=['bin/wait_service'],
    install_requires=['scipy']
)

# coding: utf-8
import codecs

from setuptools import setup, find_packages

exec(open("stellar_base/version.py").read())

with codecs.open('README.rst', encoding='utf-8') as file:
    long_description = file.read()

install_requires = [
    'ed25519',
    'crc16',
    'requests',
    'stellar-base-sseclient',
    'numpy',
    'toml',
    'mnemonic',
    'six',
]
tests_require = ['pytest', 'mock', 'sphinx']

setup(
    name='stellar-base',
    version=__version__,
    description='Stellar SDK for Python',
    long_description=long_description,
    keywords=["stellar", "blockchain", "cryptocurrency"],
    url='http://github.com/stellarCN/py-stellar-base/',
    license='Apache',
    author='Eno',
    author_email='appweb.cn@gmail.com',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 0 - Alpha/unstable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=install_requires,
    tests_require=tests_require
)

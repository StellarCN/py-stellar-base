# coding: utf-8
import codecs

from setuptools import setup, find_packages

with codecs.open('README.md', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='stellar-base',
    version='0.1.10',
    description='Code for managing Stellar.org blockchain transactions and accounts using stellar-base in python. Allows full functionality interfacing with the Horizon front end. Visit https://stellar.org for more information.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["stellar.org", "lumens", "xlm", "blockchain", "distributed exchange", "cryptocurrency", "dex", "stellar-core", "horizon", "sdex", "trading"],
    url='http://github.com/stellarCN/py-stellar-base/',
    license='Apache',
    author='Eno, overcat',
    author_email='appweb.cn@gmail.com, 4catcode@gmail.com',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'ed25519', 'crc16', 'requests', 'SSEClient', 'numpy', 'toml', 'mnemonic'
    ]
)

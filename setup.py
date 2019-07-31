import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
requirements_file = 'requirements.txt'

about = {}
with open(os.path.join(here, "stellar_sdk", "__version__.py"), mode="r", encoding="utf-8") as f:
    exec(f.read(), about)

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    keywords=["stellar-sdk", "stellar.org", "lumens", "xlm", "blockchain", "distributed exchange", "cryptocurrency",
              "dex", "stellar-core", "horizon", "sdex", "trading"],
    include_package_data=True,
    install_requires=open(requirements_file).readlines(),
    packages=find_packages(),
    python_requires=">=3.5.4",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

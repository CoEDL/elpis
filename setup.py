'''
Copyright: University of Queensland, 2019
Contributors:
             Nicholas Buckeridge - (University of Queensland, 2018)
             Ben Foley - (University of Queensland, 2018)
'''

from setuptools import setup, find_packages


requirements = [dependency.strip() for dependency in open("requirements.txt", "r").readlines()]

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='elpis',
    version='0.91.1',
    packages=find_packages(),
    url='https://github.com/CoEDL/elpis',
    install_requires=requirements,
    include_package_data=True,
    license='',
    author='CoEDL',
    author_email='b.foley@uq.edu.au',
    description='Scripts for preparing language data for use with Kaldi ASR',
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Topic :: Text Processing :: Linguistic",
        "Operating System :: Linux",
    ],
    entry_points={
    },
)
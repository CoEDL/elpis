'''
Copyright: University of Queensland, 2019
Contributors:
             Nicholas Lambourne - (University of Queensland, 2019)
             Ben Foley - (University of Queensland, 2019)
             Robert Cochran - (University of Queensland, 2019)
             Nicholas Buckeridge - (University of Queensland, 2019)
             Emmanuel Tope-Ojo - (University of Queensland, 2019)
             Rah Sanders-Dwyer - (University of Queensland, 2019)
'''

from setuptools import setup, find_packages


requirements = [dependency.strip() for dependency in open("requirements.txt", "r").readlines()]

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='elpis',
    version='0.94.1',
    packages=find_packages(),
    url='https://github.com/CoEDL/elpis',
    install_requires=requirements,
    include_package_data=True,
    license='',
    author='CoEDL',
    author_email='b.foley@uq.edu.au',
    description='',
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Topic :: Text Processing :: Linguistic",
        "Operating System :: Linux",
    ],
    entry_points={
    },
)
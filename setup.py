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


requirements = [
    'Flask',
    'werkzeug',
    'kaldi-helpers'
]

package_data = {

}

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='elpis',
    version='0.90',
    packages=find_packages(),
    url='https://github.com/CoEDL/elpis',
    install_requires=requirements,
    include_package_data=False,
    license='',
    author='CoEDL',
    author_email='n.lambourne@uq.edu.au',
    description='An environment and interface for accelerating linguistic transcription',
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Topic :: Text Processing :: Linguistic",
        "Operating System :: Linux",
    ],
    entry_points={
    },
)
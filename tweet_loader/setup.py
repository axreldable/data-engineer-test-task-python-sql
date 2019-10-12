import os

from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(
    name='tweet-loader',
    version='1.0.0',
    packages=[
        'bin',
        'tweet_loader',
    ],
    description='Project to load tweets.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    scripts=['bin/tweet_loader'],
    install_requires=[
    ],
    tests_require=[
        'nose',
    ],
)

# python setup.py sdist

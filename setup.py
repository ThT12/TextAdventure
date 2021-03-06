from setuptools import setup, find_packages
from codecs import open


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    my_license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='TextAdventure',
    version='1.0.0',
    description='A simple game to discover Python language',
    long_description=readme,
    url='https://github.com/ThT12/TextAdventure',
    author='Romain ThT12 Bourget',
    author_email='romain@bourget-olivier.fr',
    license=my_license,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Beginner',
        'Topic :: Discovery',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='discover python language',
    packages=find_packages(exclude=['tests']),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'play_text_adventure=textadventure.adventure:main',
        ],
    },
)

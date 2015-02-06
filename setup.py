"""
Foundry
-----------------

A tool to help manage and populate application data stores for development and
testing environments.
"""
from setuptools import setup

setup(
    name='foundry',
    version='0.0.3',
    packages=['foundry'],
    url='http://github.com/eriktaubeneck/foundry',
    license='MIT',
    author='Erik Taubeneck',
    author_email='erik.taubeneck@gmail.com',
    description='Casting objects from seed data.',
    long_description=__doc__,
    py_modules=['foundry'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'pyyaml >=3.0, <4.a0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English ',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

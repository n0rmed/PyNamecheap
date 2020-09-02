#!/usr/bin/env python3
import warnings
import namecheap
from os.path import join, dirname
from setuptools import find_packages, setup


BASE_DIR = dirname(__file__)
MOD_DIR = join(BASE_DIR, 'namecheap')
INIT_FILE = join(MOD_DIR, '__init__.py')


with open(join(BASE_DIR, "README.md"), "r") as fh:
    long_description = fh.read()

extra_commands = {}

try:
    # noinspection PyUnresolvedReferences
    import privex.helpers.setuppy.commands
    from privex.helpers import settings

    settings.VERSION_FILE = INIT_FILE

    extra_commands['extras'] = privex.helpers.setuppy.commands.ExtrasCommand
    extra_commands['bump'] = privex.helpers.setuppy.commands.BumpCommand
except (ImportError, AttributeError) as e:
    warnings.warn('Failed to import privex.helpers.setuppy.commands - the commands "extras" and "bump" may not work.')
    warnings.warn(f'Error Reason: {type(e)} - {str(e)}')


extra_packages = {
    'py36': ['dataclasses>=0.7'],
    'dataclasses': ['dataclasses>=0.7'],
    'dev': ['setuptools', 'wheel', 'twine', 'nose', 'privex-helpers[setuppy]'],
}


setup(
    name='privex_namecheap',
    version=namecheap.VERSION,
    url='https://github.com/Privex/PyNamecheap',
    license='MIT',
    author='Privex Inc.',
    author_email='company@privex.io',
    description='Namecheap API client in Python (fork of Bemmu/PyNamecheap)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['namecheap'],
    packages=find_packages(exclude=[
        'tests', 'tests.*', 'test.*', 'namecheap_tests.py'
    ]),
    scripts=['namecheap-api-cli'],
    platforms='any',
    install_requires=[
        'requests',
        'privex-helpers>=2.18.0',
        'privex-loghelper',
    ],
    cmdclass=extra_commands,
    extras_require=extra_packages,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

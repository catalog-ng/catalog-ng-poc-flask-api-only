## CKAN 3.0 (poc)

import sys
from pkg_resources import normalize_path
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = '3.0-alpha'

install_requires = [
    'Flask',
    #"Flask-OpenID",  # Maybe in the future..
    "Flask-SQLAlchemy",
    "Flask-RESTful",
    #"Flask-Restless",  # ?
    "psycopg2",
    "six", # This is apparently needed..
]

tests_require = [
    'pytest',
    'pytest-pep8',
    'pytest-cov',
]

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--ignore=build',
            '--pep8',
            '.']
        self.test_suite = True

    def run_tests(self):
        from pkg_resources import _namespace_packages
        import pytest

        # Purge modules under test from sys.modules. The test loader will
        # re-import them from the build location. Required when 2to3 is used
        # with namespace packages.
        if sys.version_info >= (3,) and \
                getattr(self.distribution, 'use_2to3', False):
            module = self.test_args[-1].split('.')[0]
            if module in _namespace_packages:
                del_modules = []
                if module in sys.modules:
                    del_modules.append(module)
                module += '.'
                for name in sys.modules:
                    if name.startswith(module):
                        del_modules.append(name)
                map(sys.modules.__delitem__, del_modules)

            ## Run on the build directory for 2to3-built code..
            ei_cmd = self.get_finalized_command("egg_info")
            self.test_args = [normalize_path(ei_cmd.egg_base)]

        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='ckan',
    version=version,
    packages=find_packages(),
    url='',
    license='GNU Affero General Public License v3',
    author='Samuele Santi',
    author_email='samuele@samuelesanti.com',
    description='CKAN 3.0 proof-of-concept',
    long_description='CKAN 3.0 profof-of-concept',
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='ckan.tests',
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 2.7",
    ],
    package_data={'': ['README.md', 'LICENSE']},
    cmdclass={'test': PyTest},
    **extra
)

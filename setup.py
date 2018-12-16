# core modules
from setuptools import find_packages
from setuptools import setup
import io
import os
import unittest

# internal modules
exec(open('model_lab/_version.py').read())


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()


def my_test_suite():
    """Return a a composite test consisting of a number of TestCases."""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


config = {
    'name': 'model_lab',
    'version': __version__,
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'maintainer': 'Martin Thoma',
    'maintainer_email': 'info@martin-thoma.de',
    'packages': find_packages(),
    'scripts': ['bin/model_lab'],
    'platforms': ['Linux'],
    'url': 'https://github.com/MartinThoma/model-lab',
    'download_url': 'https://github.com/MartinThoma/model-lab',
    'license': 'MIT',
    'description': 'model_lab helps machine learning developers to make '
                    'models accessible for humans.',
    'long_description': read('README.md'),
    'long_description_content_type': 'text/markdown',
    'install_requires': ['flask'],
    'keywords': ['utility'],
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    'classifiers': ['Development Status :: 1 - Planning',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Natural Language :: English',
                    'Programming Language :: Python :: 3.6',
                    ],
    'zip_safe': True,
    'test_suite': 'setup.my_test_suite',
}

setup(**config)

from setuptools import setup, find_packages
import sys, os

version = '0.1'

tests_require = [
    'pytest-cov',
    'pytest',
]

setup(name='kotti_blog',
      version=version,
      description="Kotti blog",
      long_description="""\
A blog addon for kotti""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='kotti blog',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['Kotti>=0.5.1'] + tests_require,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

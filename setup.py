from setuptools import setup, find_packages
import os

version = '0.3.1'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
AUTHORS = open(os.path.join(here, 'AUTHORS.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

long_description = (
    README
    + '\n' +
    AUTHORS
    + '\n' +
    CHANGES
)

setup(name='kotti_blog',
      version=version,
      description="Add a simple blog to your Kotti site",
      long_description=long_description,
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Pylons',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: Repoze Public License',
      ],
      keywords='kotti blog',
      author='Marco Scheidhuber',
      author_email='j23d@jusid.de',
      url='http://pypi.python.org/pypi/kotti_blog',
      license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Kotti>=0.8a1',
          'plone.batching',
          'AccessControl',  # this is actually a dependency of plone.batching
          'js.jquery_infinite_ajax_scroll',
          'python-dateutil',
      ],
      entry_points="""
      [fanstatic.libraries]
      kotti_blog = kotti_blog.fanstatic:library
      """,
      extras_require={},
      message_extractors={'kotti_blog': [
            ('**.py', 'lingua_python', None),
            ('**.zcml', 'lingua_xml', None),
            ('**.pt', 'lingua_xml', None),
            ]},
      )

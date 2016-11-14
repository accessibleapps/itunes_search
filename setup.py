from setuptools import setup

__version__ = 0.3
__author__ = 'Christopher Toth'
__doc__ = """Simple wrapper over the iTunes search API"""


setup(
 name = 'itunes_search',
 version = str(__version__),
 description = __doc__,
 py_modules = ['itunes_search'],
 zip_safe=False,
 install_requires = [
  'requests',
 ],
 classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'License :: OSI Approved :: MIT License',
  'Topic :: Software Development :: Libraries',
 ],
)

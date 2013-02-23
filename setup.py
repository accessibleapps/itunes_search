from setuptools import setup
import itunes_search

setup(
 name = itunes_search.__name__,
 version = str(itunes_search.__version__),
 description = itunes_search.__doc__,
 py_modules = ['itunes_search'],
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

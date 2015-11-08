from setuptools import setup

__version__ = '0.0.0'

try:
    with open('README.rst') as f:
        long_description = f.read()
except IOError:
    long_description = 'Simple library to support live coding'

config = {
    'name': 'live',
    'version': __version__,
    'description': 'Simple library to support live coding',
    'long_description': long_description,
    'author': 'Fritz Obermeyer',
    'author_email': 'fritz.obermeyer@gmail.com',
    'url': 'https://github.com/fritzo/livecoder',
    'py_modules': ['live'],
}

setup(**config)

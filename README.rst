Livecoder
=========

.. image:: https://travis-ci.org/fritzo/livecoder.png?branch=master
   :target: https://travis-ci.org/fritzo/livecoder
   :alt: Build status

.. image:: https://badge.fury.io/py/live.png
   :target: https://pypi.python.org/pypi/live
   :alt: PyPI Version

A simple library to support live coding in python.
Modeled after the idioms in `livecoder.net`_.

.. _`livecoder.net`: http://livecoder.net

Quick Start
-----------

Install livecoder from pypi::

  pip install live

Open an example file with your favorite editor::

  git clone git@github.com:fritzo/livecoder     # grab an example
  vi livecoder/examples/datadiff.py             # open in your favorite editor

And tell ``live`` to watch the script::

  cd livecoder/examples                 # move to where script is importable
  live datadiff.py                      # and watch output for errors

Every time you save the script, ``live`` reloads it and updates the live coding
state.
You'll probably want to set up your editor to save after every keystroke, or
save once per second.
For example in Vim 7.4+ you can save after each modification using::

  autocmd TextChanged,TextChangedI <buffer> write

License
-------

`Apache 2.0`_

.. _`Apache 2.0`: LICENSE

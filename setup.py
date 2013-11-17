#!/usr/bin/env python

from distutils.core import setup
from iggy import __version__ as VERSION

setup(name='iggy',
      version=VERSION,
      description="""py3 irc bot""",
      author='Adam Stokes',
      author_email='adam.stokes@ubuntu.com',
      url='https://github.com/battlemidget/iggy',
      license="MIT",
      scripts=['iggybot'],
      packages=['iggy'],
      requires=['circuits'],
     )


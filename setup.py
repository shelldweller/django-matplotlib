#!/usr/bin/env python
from distutils.core import setup

setup(
    name = 'django-matplotlib',
    description = '''Django interface to matplotlib''',
    version = '0.1-pre-alpha',
    author = 'Sergiy Kuzmenko',
    author_email = 'sergiy@kuzmenko.org',
    url = 'https://github.com/shelldweller/django-matplotlib',
    packages=['django_matplotlib'],
    classifiers = ['Development Status :: 2 - Pre-Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: Public Domain',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   ],
)

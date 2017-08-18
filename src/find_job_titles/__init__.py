# -*- coding: utf-8 -*-

"""
Module for find_job_titles library.

TODO:
* startup time is far too long; need to reduce size of job titles file
* sort job titles by corpus frequency, so that we can load only top-N titles
* ideally test job titles against a real-world corpus to weed out irrelevant
 titles
* function to return only longest match?
"""

__author__ = 'Johannes Ahlmann'
__email__ = 'johannes@fluquid.com'
__version__ = '0.3.0-dev'

import gzip
from pkg_resources import resource_stream
import logging

from acora import AcoraBuilder


def load_titles():
    with resource_stream('find_job_titles',
                         'data/titles_combined.txt.gz') as fhandle:
        with gzip.GzipFile(fileobj=fhandle, mode='r') as gzf:
            for line in gzf:
                yield line.decode('utf-8').strip()


class Finder(object):
    """
    Finder class.
    """
    def __init__(self, use_unicode=True):
        titles = (load_titles()
                  if use_unicode
                  else (s.encode('ascii') for s in load_titles()))
        builder = AcoraBuilder()
        logging.warn('building job title searcher')
        builder.update(titles)
        logging.warn('building done')
        self.ac = builder.build()

    def findall(self, string):
        return self.ac.findall(string)

    def finditer(self, string):
        return self.ac.finditer(string)

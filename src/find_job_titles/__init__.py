# -*- coding: utf-8 -*-

__author__ = 'Johannes Ahlmann'
__email__ = 'johannes@fluquid.com'
__version__ = '0.1.0'

import gzip
from pkg_resources import resource_stream
import logging

from acora import AcoraBuilder


def load_titles():
    with resource_stream('find_job_titles',
                         'data/titles_combined.txt.gz') as fhandle:
        with gzip.open(fhandle, 'rt') as gzf:
            for line in gzf:
                yield line.strip()


class Finder(object):
    """
    Finder class.
    FIXME: subclass Acora class? which one?
    """
    def __init__(self, use_ascii=False):
        titles = (load_titles()
                  if not use_ascii
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

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
__version__ = '0.5.0'

import gzip
from pkg_resources import resource_stream
import logging
from itertools import groupby

from acora import AcoraBuilder


def load_titles():
    with resource_stream('find_job_titles',
                         'data/titles_combined.txt.gz') as fhandle:
        with gzip.GzipFile(fileobj=fhandle, mode='r') as gzf:
            for line in gzf:
                # Note: decode rather than "rt" for py2 compat
                yield line.decode('utf-8').strip()


class FinderAcora(object):
    """
    Finder class based on "acora" library.

    building data structure takes a moment, and having issues
        with finding longest matches.
    """
    def __init__(self, use_unicode=True, ignore_case=False):
        titles = (load_titles()
                  if use_unicode
                  else (s.encode('ascii') for s in load_titles()))
        builder = AcoraBuilder()
        logging.info('building job title searcher')
        builder.update(titles)
        self.ac = builder.build(ignore_case=ignore_case)
        logging.info('building done')

    def search_longest(self, matches):
        # source: https://github.com/scoder/acora#faqs-and-recipes
        for pos, match_set in groupby(matches, lambda x: len(x[0]) + x[1]):
            yield max(match_set, key=lambda x: len(x))

    def findall(self, string):
        return list(self.search_longest(self.ac.findall(string)))

    def finditer(self, string):
        return self.search_longest(self.ac.finditer(string))


class Finder(FinderAcora):
    pass

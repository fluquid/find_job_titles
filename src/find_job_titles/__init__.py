# -*- coding: utf-8 -*-

"""
The `find_job_titles` library finds mentions of job titles in strings.

In order to do so it compiles a search datastructure (Aho Corasick) and uses
    a precompiled list of >70k job titles as a reference list.

It returns the longest matching job title, including cross-overlapping matches,
    together with the start and end position in the given string.

TODO:
* also compare to https://github.com/scrapinghub/webstruct/blob/master/webstruct/utils.py#L155
"""

__author__ = 'Johannes Ahlmann'
__email__ = 'johannes@fluquid.com'
__version__ = '0.7.1'

import gzip
from pkg_resources import resource_stream
import logging
from collections import namedtuple

from acora import AcoraBuilder
import ahocorasick


Match = namedtuple('Match', ['start', 'end', 'match'])


def load_titles():
    """
    load job titles as generator from txt.gz file included in the library
    """
    with resource_stream('find_job_titles',
                         'data/titles_combined.txt.gz') as fhandle:
        with gzip.GzipFile(fileobj=fhandle, mode='r') as gzf:
            for line in gzf:
                # Note: decode rather than "rt" for py2 compat
                # TODO: using pyahocorasick this should now be 'str' again ;(
                yield line.decode('utf-8').strip()


def longest_match(matches):
    """
    find respective longest matches from all overlapping aho corasick matches
    """
    try:
        longest = next(matches)
        if longest is None:
            return
    except StopIteration:
        return

    for elt in matches:
        # if (a contains b) or (b contains a)
        if (elt.start >= longest.start and elt.end <= longest.end) or \
           (longest.start >= elt.start and longest.end <= elt.end):
            longest = max(longest, elt, key=lambda x: x.end - x.start)
        else:
            yield longest
            longest = elt
    yield longest


def add_start(matches):
    """
    convert acora `(match, start)` tuples into `Match(start, end, match)` format
    """
    return (Match(start=start, end=start + len(match), match=match)
            for match, start in matches)


class BaseFinder(object):
    """
    Base class containing query methods
    """

    def findall(self, string, use_longest=True):
        """
        utility function returning `list` of results from `finditer`
        :param string: string to search target patterns in
        :param use_longest: if True only return longest matches,
                            else return all overlapping matches
        :returns: list of matches of type `Match`
        """
        return list(self.finditer(string, use_longest=use_longest))

    def finditer(self, string, use_longest=True):
        """
        iterator of all (longest) matches of target patterns in `string`
        :param string: string to search target patterns in
        :param use_longest: if True only return longest matches,
                            else return all overlapping matches
        :returns: generator of matches of type `Match`
        """
        if use_longest:
            return longest_match(self.find_raw(string))
        else:
            return self.find_raw(string)


class FinderAcora(BaseFinder):
    """
    Finder class based on "acora" library.

    Note: Building data structure seems to be significantly slower than with
          pyahocorasick
    """

    def __init__(self, use_unicode=True, ignore_case=False, titles=None, extra_titles=None):
        """
        :param use_unicode: whether to use `titles` as unicode or bytestrings
        :param ignore_case: if True ignore case in all matches
        :param titles: if given, overrides default `load_titles()` values
        :param extra_titles: if given, add to titles
        """
        titles = titles if titles else load_titles()
        titles = (titles
                  if use_unicode
                  else (s.encode('ascii') for s in titles))
        builder = AcoraBuilder()
        logging.info('building job title searcher')
        builder.update(titles)
        if extra_titles:
            builder.add(extra_titles)

        self.ac = builder.build(ignore_case=ignore_case)
        logging.info('building done')

    def find_raw(self, string):
        """
        generator of raw, overlapping matches of all lengths from automaton
        """
        return add_start(self.ac.finditer(string))


class FinderPyaho(BaseFinder):
    """
    Finder class based on "pyahocorasick" library.

    TODO:
    - use pickle and unpickle support for `self.autom`
    """

    def __init__(self, ignore_case=True, titles=None, extra_titles=None):
        """
        :param ignore_case if True, lower case job titles are also added
        :param titles: if given, overrides default `load_titles()` values
        :param extra_titles: if given, add to titles
        """
        titles = titles if titles else load_titles()
        logging.info('building job title searcher')
        autom = ahocorasick.Automaton()
        for title in titles:
            autom.add_word(title, title)
            if ignore_case:
                autom.add_word(title.lower(), title.lower())

        if extra_titles:
            for title in extra_titles:
                autom.add_word(title, title)
                if ignore_case:
                    autom.add_word(title.lower(), title.lower())

        autom.make_automaton()
        self.autom = autom
        logging.info('building done')

    def find_raw(self, string):
        """
        generator of raw, overlapping matches of all lengths from automaton
        """
        for end, match in self.autom.iter(string):
            start = end - len(match) + 1
            yield Match(start=start, end=end, match=match)


Finder = FinderPyaho

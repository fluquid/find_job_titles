from __future__ import unicode_literals
from find_job_titles import Finder

# FIXME: should be in setup code
finder = Finder()


def test_some_matches():
    fds = [x[0] for x in finder.finditer('I am the Senior Vice President')]
    assert fds == ['Senior Vice President']

    fds = [x[0] for x in finder.finditer('I am the Senior Vice President asdf')]
    assert fds == ['Senior Vice President']

    fds = [x[0] for x in finder.finditer('Senior Vice President I am')]
    assert fds == ['Senior Vice President']


def test_no_matches():
    assert not finder.findall('defo no matches in here')


def test_position():
    fds = [x[1] for x in finder.findall('at the end: Vice President')]
    assert fds == [12]

    fds = [x[1] for x in finder.findall(
        'in the middle Vice President of sentence')]
    assert fds == [14]

    fds = [x[1] for x in finder.findall('Vice President at the beginning')]
    assert fds == [0]


def test_overlapping():
    fds = [x[0] for x in finder.findall('Vice President & CEO')]
    assert fds == ['Vice President', 'President & CEO']


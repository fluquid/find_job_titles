from __future__ import unicode_literals
from find_job_titles import Finder

# FIXME: should be in setup code
finder = Finder()


def test_some_matches():
    fds = [x[0] for x in finder.finditer('I am the Senior Vice President')]
    assert fds == ['Senior Vice President', 'Vice President', 'President']


def test_no_matches():
    assert not finder.findall('defo no matches in here')


def test_position():
    fds = [x[1] for x in finder.findall('asdf sdksa President')]
    assert fds == [11]

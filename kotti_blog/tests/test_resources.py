# -*- coding: utf-8 -*-

from kotti.resources import get_root
from kotti.testing import DummyRequest

from kotti_blog.resources import Blog
from kotti_blog.resources import BlogEntry


def test_blog(kotti_blog_populate_settings,
              db_session, dummy_request, config):
    import datetime
    from dateutil.tz import tzutc
    from kotti.resources import get_root
    from kotti_blog.resources import Blog, BlogEntry

    root = get_root()
    root['blog'] = Blog(u'Blog')
    root['blog']['a'] = BlogEntry(title=u'Old one',
                                  date=datetime.datetime(2012, 7, 28,
                                                         tzinfo=tzutc()))
    root['blog']['a'].tags = [u'a', u'b', u'a b']
    root['blog']['b'] = BlogEntry(title=u'Old two',
                                  date=datetime.datetime(2012, 7, 29,
                                                         tzinfo=tzutc()))
    root['blog']['b'].tags = [u'b', u'a b']
    root['blog']['c'] = BlogEntry(title=u'New one',
                                  date=datetime.datetime(2013, 7, 7,
                                                         tzinfo=tzutc()))
    root['blog']['c'].tags = [u'c', u'b c']

    assert root['blog'].get_unique_tags(dummy_request) ==\
        [(u'a b', 2), (u'b', 2), (u'a', 1), (u'c', 1), (u'b c', 1)]

    assert root['blog'].get_archives(dummy_request) ==\
        [(datetime.date(2013, 7, 1), 1), (datetime.date(2012, 7, 1), 2)]

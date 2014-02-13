# -*- coding: utf-8 -*-


def test_blog_sidebar(kotti_blog_populate_settings,
                      db_session, dummy_request):

    import datetime
    from dateutil.tz import tzutc
    from kotti.resources import get_root
    from kotti_settings.util import set_setting
    from kotti_blog.resources import Blog, BlogEntry
    from kotti_blog.widgets import blog_sidebar_view

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

    set_setting('kotti_blog-use_sidebar_archives', True)
    set_setting('kotti_blog-use_sidebar_categories', True)
    sidebars = blog_sidebar_view(root['blog'], dummy_request)

    assert sidebars['unique_tags'] == [(u'a b', 2), (u'b', 2), (u'a', 1)]
    assert sidebars['archives'] ==\
        [(datetime.date(2013, 7, 1), 1), (datetime.date(2012, 7, 1), 2)]


    set_setting('kotti_blog-sidebar_categories_number', 1)
    set_setting('kotti_blog-sidebar_archives_number', 1)
    sidebars = blog_sidebar_view(root['blog'], dummy_request)
    assert sidebars['unique_tags'] == [(u'a b', 2)]
    assert sidebars['archives'] == [(datetime.date(2013, 7, 1), 1)]

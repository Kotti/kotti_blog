

def test_blog_view(kotti_blog_populate_settings,
                   db_session, dummy_request):
    from kotti.resources import get_root
    from kotti_blog.resources import Blog, BlogEntry
    from kotti_blog.views import Views

    root = get_root()
    root['blog'] = Blog(u'Blog')
    root['blog']['a'] = BlogEntry()
    root['blog']['b'] = BlogEntry()
    view = Views(root['blog'], dummy_request)
    result = view.view_blog()

    assert result['macros'] is not None
    assert result['use_pagination'] is True
    assert result['api'] is not None
    assert result['link_headline'] is True
    assert len(result['items']) == 2


def test_use_auto_pagination_view(kotti_blog_populate_settings,
                                  db_session, dummy_request):
    from kotti.resources import get_root
    from kotti_blog.views import use_auto_pagination

    result = use_auto_pagination(get_root(), dummy_request)
    assert result['use_auto_pagination'] is False

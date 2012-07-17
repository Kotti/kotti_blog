from pyramid.threadlocal import get_current_registry
from kotti.testing import FunctionalTestBase
from kotti_blog import blog_settings


class TestBlog(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_blog.kotti_configure',
                    'kotti_blog.blog_settings.pagesize': '5'}
        super(TestBlog, self).setUp(**settings)

    def test_blog_default_settings(self):
        b_settings = blog_settings()
        assert b_settings['use_batching'] == True
        assert b_settings['pagesize'] == 5
        assert b_settings['use_auto_batching'] == True
        assert b_settings['link_headline_overview'] == True

    def test_blog_change_settings(self):
        settings = get_current_registry().settings
        settings['kotti_blog.blog_settings.use_batching'] = u'false'
        settings['kotti_blog.blog_settings.pagesize'] = u'2'
        settings['kotti_blog.blog_settings.use_auto_batching'] = u'false'
        settings['kotti_blog.blog_settings.link_headline_overview'] = u'false'

        b_settings = blog_settings()
        assert b_settings['use_batching'] == False
        assert b_settings['pagesize'] == 2
        assert b_settings['use_auto_batching'] == False
        assert b_settings['link_headline_overview'] == False

    def test_blog_wrong_settings(self):
        settings = get_current_registry().settings
        settings['kotti_blog.blog_settings.use_batching'] = u'blibs'
        settings['kotti_blog.blog_settings.pagesize'] = u'blabs'
        settings['kotti_blog.blog_settings.use_auto_batching'] = u'blubs'
        settings['kotti_blog.blog_settings.link_headline_overview'] = u'blobs'

        b_settings = blog_settings()
        assert b_settings['use_batching'] == False
        assert b_settings['pagesize'] == 5
        assert b_settings['use_auto_batching'] == False
        assert b_settings['link_headline_overview'] == False

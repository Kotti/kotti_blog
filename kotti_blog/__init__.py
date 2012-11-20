from pyramid.i18n import TranslationStringFactory
from kotti.util import extract_from_settings

_ = TranslationStringFactory('kotti_blog')


def kotti_configure(settings):
    settings['pyramid.includes'] += ' kotti_blog.views'
    settings['kotti.available_types'] += ' kotti_blog.resources.Blog kotti_blog.resources.BlogEntry'


def check_true(value):
    if value == u'true':
        return True
    return False


BLOG_DEFAULTS = {
    'use_batching': 'true',
    'pagesize': '5',
    'use_auto_batching': 'true',
    'link_headline_overview': 'true',
    }


def blog_settings(name=''):
    prefix = 'kotti_blog.blog_settings.'
    if name:
        prefix += name + '.'  # pragma: no cover
    settings = BLOG_DEFAULTS.copy()
    settings.update(extract_from_settings(prefix))
    settings['use_batching'] = check_true(settings['use_batching'])
    try:
        settings['pagesize'] = int(settings['pagesize'])
    except ValueError:
        settings['pagesize'] = 5
    settings['use_auto_batching'] = check_true(settings['use_auto_batching'])
    settings['link_headline_overview'] = check_true(settings['link_headline_overview'])

    return settings

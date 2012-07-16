from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('kotti_blog')


def kotti_configure(settings):
    settings['pyramid.includes'] += ' kotti_blog.views'
    settings['kotti.available_types'] += ' kotti_blog.resources.Blog kotti_blog.resources.BlogEntry'

from fanstatic import Library
from fanstatic import Resource
from pyramid.i18n import TranslationStringFactory
from kotti.static import view_needed

_ = TranslationStringFactory('kotti_blog')

library = Library("kotti_navigation", "static")
kotti_navigation_css = Resource(library, "style.css")
view_needed.add(kotti_navigation_css)


def kotti_configure(settings):
    settings['pyramid.includes'] += ' kotti_blog.views'
    settings['kotti.available_types'] += ' kotti_blog.resources.Blog kotti_blog.resources.BlogEntry'

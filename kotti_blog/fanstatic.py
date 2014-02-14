# -*- coding: utf-8 -*-

from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.jquery_infinite_ajax_scroll import jquery_infinite_ajax_scroll
from js.jquery_infinite_ajax_scroll import jquery_infinite_ajax_scroll_css

from kotti.fanstatic import view_needed


library = Library("kotti_blog", "static")

kotti_blog_css = Resource(
    library,
    "style.css",
    depends=[jquery_infinite_ajax_scroll_css, ],
    minified='style.min.css',
    bottom=True
)
kotti_blog_js = Resource(
    library,
    "kotti_blog.js",
    depends=[jquery_infinite_ajax_scroll, ],
    minified='kotti_blog.min.js',
    bottom=True
)
group = [kotti_blog_css, kotti_blog_js]
view_needed.add(Group(group))

social_privacy_css = Resource(
    library,
    "socialshareprivacy/socialshareprivacy.css",
    minified='socialshareprivacy/socialshareprivacy.min.css',
    bottom=True
)
social_privacy_js = Resource(
    library,
    "socialshareprivacy/jquery.socialshareprivacy.js",
    minified='socialshareprivacy/jquery.socialshareprivacy.min.js',
    depends=[social_privacy_css],
    bottom=True
)
social_privacy_en_js = Resource(
    library,
    "socialshareprivacy/jquery.socialshareprivacy.en.js",
    minified='socialshareprivacy/jquery.socialshareprivacy.en.min.js',
    depends=[social_privacy_js],
    bottom=True
)
social_privacy_de_js = Resource(
    library,
    "socialshareprivacy/jquery.socialshareprivacy.de.js",
    minified='socialshareprivacy/jquery.socialshareprivacy.de.min.js',
    depends=[social_privacy_js],
    bottom=True
)

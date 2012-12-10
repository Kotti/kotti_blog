# -*- coding: utf-8 -*-

from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.jquery_infinite_ajax_scroll import jquery_infinite_ajax_scroll
from js.jquery_infinite_ajax_scroll import jquery_infinite_ajax_scroll_css

from kotti.fanstatic import view_needed


library = Library("kotti_blog", "static")
kotti_blog_css = Resource(library,
    "style.css",
    depends=[jquery_infinite_ajax_scroll_css, ],
    minified='style.min.css',
    bottom=True)
kotti_blog_js = Resource(library,
    "kotti_blog.js",
    depends=[jquery_infinite_ajax_scroll, ],
    minified='kotti_blog.min.js',
    bottom=True)
view_needed.add(Group([kotti_blog_css, kotti_blog_js, ]))

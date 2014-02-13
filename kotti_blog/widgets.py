from pyramid.view import view_config
from pyramid.exceptions import PredicateMismatch

from kotti.views.slots import assign_slot
from kotti.views.util import template_api

from kotti_settings.util import get_setting

from kotti_blog.resources import Blog
from kotti_blog.resources import BlogEntry


@view_config(name="blog_sidebar",
             renderer="kotti_blog:templates/blog-sidebar.pt")
def blog_sidebar_view(context, request):
    # Only show sidebar on Blog and Blog Entries
    if not (isinstance(context, Blog) or isinstance(context, BlogEntry)):
        raise PredicateMismatch()

    # Find the blog

    if isinstance(context, Blog):
        blog = context
    else:
        blog = context.parent

    api = template_api(context, request)

    use_categories = get_setting('use_sidebar_categories')
    unique_tags = None
    if use_categories:
        number = get_setting('sidebar_categories_number')
        if number:
            unique_tags = blog.get_unique_tags(request)[:number]
        else:
            unique_tags = blog.get_unique_tags(request)

    use_archives = get_setting('use_sidebar_archives')
    archives = None
    if use_archives:
        number = get_setting('sidebar_archives_number')
        if number:
            archives = blog.get_archives(request)[:number]
        else:
            archives = blog.get_archives(request)

    return {
        'blog_url': api.url(blog),
        'unique_tags': unique_tags,
        'use_categories': use_categories,
        'archives': archives,
        'use_archives': use_archives,
    }


def includeme(config):
    config.scan(__name__)
    assign_slot('blog_sidebar', 'right')

from kotti import DBSession
from kotti.views.edit import DocumentSchema
from kotti.views.edit import generic_edit
from kotti.views.edit import generic_add
from kotti.views.view import view_node
from kotti.views.util import ensure_view_selector
from kotti.views.util import template_api

from kotti_blog.resources import Blog
from kotti_blog.resources import BlogEntry


class BlogSchema(DocumentSchema):
    pass


class BlogEntrySchema(DocumentSchema):
    pass


@ensure_view_selector
def edit_blog(context, request):
    return generic_edit(context, request, BlogSchema())


def add_blog(context, request):
    return generic_add(context, request, BlogSchema(), Blog, u'blog')


@ensure_view_selector
def edit_blogentry(context, request):
    return generic_edit(context, request, BlogEntrySchema())


def add_blogentry(context, request):
    return generic_add(context, request, BlogEntrySchema(), BlogEntry, u'blogentry')


def view_blog(context, request):
    session = DBSession()
    query = session.query(BlogEntry).filter(BlogEntry.parent_id == context.id)
    blogentries = query.all()

    return {
        'api': template_api(context, request),
        'blogentries': blogentries,
        }


def includeme_edit(config):

    config.add_view(
        edit_blog,
        context=Blog,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        add_blog,
        name=Blog.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        edit_blogentry,
        context=BlogEntry,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        add_blogentry,
        name=BlogEntry.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )


def includeme_view(config):
    config.add_view(
        view_blog,
        context=Blog,
        name='view',
        permission='view',
        renderer='templates/blog-view.pt',
        )

    config.add_view(
        view_node,
        context=BlogEntry,
        name='view',
        permission='view',
        renderer='templates/blogentry-view.pt',
        )

    config.add_static_view('static-kotti_blog', 'kotti_blog:static')


def includeme(config):
    includeme_edit(config)
    includeme_view(config)

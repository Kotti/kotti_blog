import datetime
from dateutil.tz import tzutc
from plone.batching import Batch
from pyramid.renderers import get_renderer
import colander
from deform.widget import DateTimeInputWidget

from kotti import DBSession
from kotti.views.edit import (
    DocumentSchema,
    generic_edit,
    generic_add,
)
from kotti.views.util import (
    ensure_view_selector,
    template_api,
    format_date,
)

from kotti_blog.resources import (
    Blog,
    BlogEntry,
)
from kotti_blog import (
    blog_settings,
    _,
)


class BlogSchema(DocumentSchema):
    pass


@colander.deferred
def deferred_date_missing(node, kw):
    value = datetime.datetime.now()
    return datetime.datetime(value.year, value.month, value.day, value.hour,
        value.minute, value.second, value.microsecond, tzinfo=tzutc())


class BlogEntrySchema(DocumentSchema):
    date = colander.SchemaNode(
        colander.DateTime(),
        title=_(u'Date'),
        description=_(u'Choose date of the blog entry. '\
                      u'If you leave this empty the creation date is used.'),
        validator=colander.Range(
            min=datetime.datetime(2012, 1, 1, 0, 0, tzinfo=colander.iso8601.Utc()),
            min_err=_('${val} is earlier than earliest datetime ${min}')),
        widget=DateTimeInputWidget(),
        missing=deferred_date_missing,
    )


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


def view_blogentry(context, request):
    context.formatted_date = format_date(context.date)
    return {}


def view_blog(context, request):
    settings = blog_settings()
    macros = get_renderer('templates/macros.pt').implementation()
    session = DBSession()
    query = session.query(BlogEntry).filter(\
                BlogEntry.parent_id == context.id).order_by(BlogEntry.date.desc())
    items = query.all()
    page = request.params.get('page', 1)
    if settings['use_batching']:
        items = Batch.fromPagenumber(items,
                      pagesize=settings['pagesize'],
                      pagenumber=int(page))

    for item in items:
        item.formatted_date = format_date(item.date)

    return {
        'api': template_api(context, request),
        'macros': macros,
        'items': items,
        'settings': settings,
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
        view_blogentry,
        context=BlogEntry,
        name='view',
        permission='view',
        renderer='templates/blogentry-view.pt',
        )

    config.add_static_view('static-kotti_blog', 'kotti_blog:static')


def includeme(config):
    settings = config.get_settings()
    if 'kotti_blog.asset_overrides' in settings:
        for override in [a.strip()
                         for a in settings['kotti_blog.asset_overrides'].split()
                         if a.strip()]:
            config.override_asset(to_override='kotti_blog', override_with=override)
    includeme_edit(config)
    includeme_view(config)

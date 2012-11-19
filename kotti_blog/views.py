import datetime
from dateutil.tz import tzutc

import colander
from deform.widget import DateTimeInputWidget
from plone.batching import Batch
from pyramid.renderers import get_renderer
from pyramid.view import view_config
from pyramid.view import view_defaults


from kotti import DBSession
from kotti.security import has_permission
from kotti.views.edit import DocumentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.views.util import template_api

from kotti_blog.resources import Blog
from kotti_blog.resources import BlogEntry
from kotti_blog import blog_settings
from kotti_blog import _


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


class BlogAddForm(AddFormView):
    schema_factory = BlogSchema
    add = Blog
    item_type = _(u"Blog")


class BlogEditForm(EditFormView):
    schema_factory = BlogSchema


class BlogEntryAddForm(AddFormView):
    schema_factory = BlogEntrySchema
    add = BlogEntry
    item_type = _(u"Blog Entry")


class BlogEntryEditForm(EditFormView):
    schema_factory = BlogEntrySchema


@view_defaults(name='view', permission='view')
class Views:

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(context=Blog,
                 renderer='kotti_blog:templates/blog-view.pt')
    def view_blog(self):
        settings = blog_settings()
        macros = get_renderer('templates/macros.pt').implementation()
        session = DBSession()
        query = session.query(BlogEntry).filter(\
                    BlogEntry.parent_id == self.context.id).order_by(BlogEntry.date.desc())
        items = query.all()
        items = [item for item in items if has_permission('view', item, self.request)]
        page = self.request.params.get('page', 1)
        if settings['use_batching']:
            items = Batch.fromPagenumber(items,
                          pagesize=settings['pagesize'],
                          pagenumber=int(page))
        return {
            'api': template_api(self.context, self.request),
            'macros': macros,
            'items': items,
            'settings': settings,
            }

    @view_config(context=BlogEntry,
                 renderer='kotti_blog:templates/blogentry-view.pt')
    def view_blogentry(self):
        return {}


def includeme_edit(config):

    config.add_view(
        BlogAddForm,
        name=Blog.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        BlogEditForm,
        context=Blog,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        BlogEntryAddForm,
        name=BlogEntry.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        BlogEntryEditForm,
        context=BlogEntry,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )


def includeme(config):
    settings = config.get_settings()
    if 'kotti_blog.asset_overrides' in settings:
        for override in [a.strip()
                         for a in settings['kotti_blog.asset_overrides'].split()
                         if a.strip()]:
            config.override_asset(to_override='kotti_blog', override_with=override)
    includeme_edit(config)
    config.add_static_view('static-kotti_blog', 'kotti_blog:static')
    config.scan(__name__)

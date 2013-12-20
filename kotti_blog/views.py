import datetime
from dateutil.tz import tzutc

import colander
from deform.widget import DateTimeInputWidget
from pyramid.renderers import get_renderer
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.exceptions import PredicateMismatch

from kotti import DBSession
from kotti.security import has_permission
from kotti.views.edit import DocumentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.views.util import template_api
from kotti.views.slots import assign_slot

from kotti_settings.util import get_setting

from kotti_blog.batch import Batch
from kotti_blog.resources import Blog
from kotti_blog.resources import BlogEntry
from kotti_blog import _


class BlogSchema(DocumentSchema):
    pass


@colander.deferred
def deferred_date_missing(node, kw):
    value = datetime.datetime.now()
    return datetime.datetime(
        value.year, value.month, value.day, value.hour,
        value.minute, value.second, value.microsecond, tzinfo=tzutc())


class BlogEntrySchema(DocumentSchema):
    date = colander.SchemaNode(
        colander.DateTime(),
        title=_(u'Date'),
        description=_(u'Choose date of the blog entry. '
                      u'If you leave this empty the creation date is used.'),
        validator=colander.Range(
            min=datetime.datetime(
                2012, 1, 1, 0, 0, tzinfo=colander.iso8601.Utc()),
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
        macros = get_renderer('templates/macros.pt').implementation()
        query = DBSession.query(BlogEntry)
        query = query.filter(BlogEntry.parent_id == self.context.id)
        query = query.order_by(BlogEntry.date.desc())
        items = query.all()
        items = [item for item in items if has_permission('view', item, self.request)]

        selected_tag = self.request.GET.get("selected-tag")

        if selected_tag:
            # items = [it for it in items if any([i in it.tags for i in selected_tag])]
            items = [it for it in items if selected_tag in it.tags]

        page = self.request.params.get('page', 1)
        use_pagination = get_setting('use_pagination')
        if use_pagination:
            items = Batch.fromPagenumber(items,
                        pagesize=get_setting('pagesize'),
                        pagenumber=int(page))
        return {
            'api': template_api(self.context, self.request),
            'macros': macros,
            'items': items,
            'use_pagination': use_pagination,
            'link_headline': get_setting('link_headline'),
            }

    @view_config(context=BlogEntry,
                 renderer='kotti_blog:templates/blogentry-view.pt')
    def view_blogentry(self):
        return {}


@view_config(name='kotti_blog_use_auto_pagination',
             permission='edit',
             renderer='json')
def use_auto_pagination(context, request):
    return {'use_auto_pagination': get_setting('use_auto_pagination')}


@view_config(name="blog_sidebar",
             renderer="kotti_blog:templates/blog-sidebar.pt")
def blog_sidebar_view(request, context):
    # Only show sidebar on Blog and Blog Entries

    if not (isinstance(request, Blog) or isinstance(request, BlogEntry)):
        raise PredicateMismatch()

    # Find the blog

    if isinstance(request, Blog):
        blog = request
    else:
        blog = request.parent

    # Get all tags so they can be shown in the sidebar and we can filter on
    # them
    api = template_api(request, context)

    unique_tags = set()
    [unique_tags.update(child.tags) for child in blog.children]

    return {
        'blog_url': api.url(blog),
        'unique_tags': unique_tags,
    }


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
    assign_slot('blog_sidebar', 'right')
    config.scan(__name__)

from dateutil.tz import tzutc
import datetime

from deform.widget import DateTimeInputWidget
from pyramid.exceptions import PredicateMismatch
from pyramid.renderers import get_renderer
from pyramid.view import render_view_to_response
from pyramid.view import view_config
from pyramid.view import view_defaults
import colander

from kotti import DBSession
from kotti.security import has_permission
from kotti.views.edit import DocumentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.views.slots import assign_slot
from kotti.views.util import template_api
from kotti_settings.util import get_setting

from kotti_blog import _
from kotti_blog.batch import Batch
from kotti_blog.resources import Blog
from kotti_blog.resources import BlogEntry


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

    @view_config(context=Blog)
    def view_blog_super(self):
        """A super view for the blog, used to handle pagination.
        """
        api = template_api(self.context, self.request)

        # Remove everything but the extra parameters
        page = self.request.url.replace(api.url(self.context).strip('/'), '')
        page = page.strip('/')

        # Pagination only works when specifying the view
        if page.startswith('view/'):
            page = page[5:]

            if page:
                self.request.GET['page'] = page

        url_parameters_get = 'view/'
        self.request.GET['url_parameters'] = url_parameters_get

        return render_view_to_response(
            self.context,
            self.request,
            name='blog-view'
        )

    @view_config(context=Blog,
                 name='blog-view',
                 renderer='kotti_blog:templates/blog-view.pt')
    def view_blog(self):
        # Get the GET requests
        selected_tag = self.request.GET.get("selected-tag")
        selected_date = self.request.GET.get("selected-date")

        macros = get_renderer('templates/macros.pt').implementation()
        query = DBSession.query(BlogEntry)
        query = query.filter(BlogEntry.parent_id == self.context.id)
        query = query.order_by(BlogEntry.date.desc())
        items = query.all()
        items = [item for item in items
                 if has_permission('view', item, self.request)]

        # Filter on date
        if selected_date:
            year, month = map(int, selected_date.split('_'))
            items = [it for it in items
                     if it.date.year == year and it.date.month == month]

        # Filter on the tag
        if selected_tag:
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
            'url_parameters': self.request.GET.get("url_parameters")
            }

    @view_config(context=Blog,
                 name="categories")
    def view_categories_super(self):
        """A super view that either shows the list or filters by the provided
        category/tag, which we get from the URL. We use this so we can have
        URL's like:

        blog/categories (shows the list)
        blog/categories/tag1 (shows articles, filtered by tag 'tag1')
        ...

        """
        api = template_api(self.context, self.request)

        # Remove everything but the extra parameters
        url_parameters = self.request.url.replace(
            api.url(self.context) + 'categories',
            ''
        )
        url_parameters = url_parameters.strip('/')

        # If we have url parameters, take first one as tag, second one as page,
        # ignore the rest
        if url_parameters:
            url_parameters = url_parameters.split('/')
            url_parameters_get = 'categories/'
            try:
                self.request.GET['selected-tag'] = url_parameters[0]
                url_parameters_get += url_parameters[0] + '/'
                self.request.GET['page'] = url_parameters[1]
            except IndexError:
                pass

            self.request.GET['url_parameters'] = url_parameters_get

            return render_view_to_response(
                self.context,
                self.request,
                name='blog-view'
            )

        # If no tag was provided, return the categories list
        return render_view_to_response(
            self.context,
            self.request,
            name='categories-list'
        )

    @view_config(context=Blog,
                 name="categories-list",
                 renderer='kotti_blog:templates/blog-categories.pt')
    def view_categories_list(self):
        return {
            'api': template_api(self.context, self.request),
            'items': self.context.get_unique_tags(self.request)
        }

    @view_config(context=Blog,
                 name="archives")
    def view_archives_super(self):
        """A super view that either shows the list or filters by the provided
        category/tag, which we get from the URL. We use this so we can have
        URL's like:

        blog/categories (shows the list)
        blog/categories/tag1 (shows articles, filtered by tag 'tag1')
        ...

        """
        api = template_api(self.context, self.request)

        # Remove everything but the extra parameters
        url_parameters = self.request.url.replace(
            api.url(self.context) + 'archives',
            ''
        )
        url_parameters = url_parameters.strip('/')

        # If we have url parameters, take first one as tag, second one as page,
        # ignore the rest
        if url_parameters:
            url_parameters = url_parameters.split('/')
            url_parameters_get = 'archives/'
            try:
                self.request.GET['selected-date'] = url_parameters[0]
                url_parameters_get += url_parameters[0] + '/'
                self.request.GET['page'] = url_parameters[1]
            except IndexError:
                pass

            self.request.GET['url_parameters'] = url_parameters_get

            return render_view_to_response(
                self.context,
                self.request,
                name='blog-view'
            )

        # If no tag was provided, return the categories list
        return render_view_to_response(
            self.context,
            self.request,
            name='archives-list'
        )

    @view_config(context=Blog,
                 name="archives-list",
                 renderer='kotti_blog:templates/blog-archives.pt')
    def view_archives_list(self):
        return {
            'api': template_api(self.context, self.request),
            'items': self.context.get_archives(self.request)
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

    return {
        'blog_url': api.url(blog),
        'unique_tags': blog.get_unique_tags(request),
        'dates': blog.get_archives(request),
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

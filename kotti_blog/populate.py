import colander

from kotti_settings.util import add_settings
from kotti_blog import _


class UsePaginationSchemaNode(colander.SchemaNode):
    name = 'use_pagination'
    title = _(u'Use pagination')
    description = _(u'Use pagination for entries on the blog.')
    missing = True
    default = True


class PagesizeSchemaNode(colander.SchemaNode):
    name = 'pagesize'
    title = _(u'Page size')
    description = _(u'Choose how many blog entries are shown '
                    u'on one page.')
    default = 5


class UseAutoPaginationSchemaNode(colander.SchemaNode):
    name = 'use_auto_pagination'
    title = _(u'Use auto pagination')
    description = _(u'Blog entries loaded automatically when scrolling '
                    u'down the blog page.')
    missing = False
    default = False


class LinkHeadlineSchemaNode(colander.SchemaNode):
    name = 'link_headline'
    title = _(u'Link headline')
    description = _(u'Control whether the headline of a blog entry in '
                    u'the blog is linked to the blog entry.')
    missing = True
    default = True


class KottiBlogSettingsSchema(colander.MappingSchema):
    use_pagination = UsePaginationSchemaNode(colander.Boolean())
    pagesize = PagesizeSchemaNode(colander.Integer())
    use_auto_pagination = UseAutoPaginationSchemaNode(colander.Boolean())
    link_headline = LinkHeadlineSchemaNode(colander.Boolean())


KottiBlogSettings = {
    'name': 'kotti_blog_settings',
    'title': _(u'Blog settings'),
    'description': _(u"Settings for kotti_blog"),
    'success_message': _(u"Successfully saved blog settings."),
    'schema_factory': KottiBlogSettingsSchema,
}


def populate_settings():
    add_settings(KottiBlogSettings)

import colander

from deform_bootstrap.widget import ChosenMultipleWidget

from kotti.views.slots import assign_slot

from kotti_settings.config import SlotSchemaNode
from kotti_settings.util import get_setting
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


class IncludeSocialSharePrivacySchemaNode(colander.SchemaNode):
    name = 'include_social'
    title = _(u'Include Social Share Privacy')
    description = _(u'Include social media buttons in the blog '
                    u'entry view. Currently facebook, twitter and '
                    u'Google+ are included.')
    missing = True
    default = True


social_media_buttons = ((u'facebook', _(u'Facebook')),
                        (u'twitter', _(u'Twitter')),
                        (u'google', _(u'Goolge+')),
                       )


class SocialMediaButtons(colander.SchemaNode):
    name=u'social_media_buttons'
    title=_(u'Social media buttons')
    description=_(u'Enable only specific social media buttons.')
    widget = ChosenMultipleWidget(values=social_media_buttons)
    default = [u'facebook', u'twitter', u'google']
    missing = [u'facebook', u'twitter', u'google']


class KottiBlogSettingsSchema(colander.MappingSchema):
    use_pagination = UsePaginationSchemaNode(colander.Boolean())
    pagesize = PagesizeSchemaNode(colander.Integer())
    use_auto_pagination = UseAutoPaginationSchemaNode(colander.Boolean())
    link_headline = LinkHeadlineSchemaNode(colander.Boolean())
    include_social = IncludeSocialSharePrivacySchemaNode(colander.Boolean())
    social_media_buttons = SocialMediaButtons(colander.Set())


KottiBlogSettings = {
    'name': 'kotti_blog_settings',
    'title': _(u'Blog settings'),
    'description': _(u"Settings for kotti_blog"),
    'success_message': _(u"Successfully saved blog settings."),
    'schema_factory': KottiBlogSettingsSchema,
}


class ShowSidebar(colander.SchemaNode):
    name = 'show_sidebar'
    title = _(u'Show sidebar')
    description = _(u'Show the sidebar in the blog view.')
    missing = True
    default = True


class UseSidebarCategories(colander.SchemaNode):
    name = 'use_sidebar_categories'
    title = _(u'Show categories in sidebar')
    description = _(u'Show categories sorted by number of posts on which you '
                    u'can filter.')
    missing = True
    default = True


class SidebarCategoriesNumber(colander.SchemaNode):
    name = 'sidebar_categories_number'
    title = _(u'The number of categories shown')
    description = _(u'Choose how many categories are shown in the sidebar. ' +
                    u'Set to 0 to show all categories.')
    default = 5


class UseSidebarArchives(colander.SchemaNode):
    name = 'use_sidebar_archives'
    title = _(u'Show archives in sidebar')
    description = _(u'Show categories sorted by date on which you can filter.')
    missing = True
    default = True


class SidebarArchivesNumber(colander.SchemaNode):
    name = 'sidebar_archives_number'
    title = _(u'The number of archives shown')
    description = _(u'Choose how many archives are shown in the sidebar. ' +
                    u'Set to 0 to show all archives.')
    default = 5


class KottiBlogSidebarSettingsSchema(colander.MappingSchema):
    show_sidebar = ShowSidebar(colander.Boolean())
    slot = SlotSchemaNode(colander.String())
    use_sidebar_categories = UseSidebarCategories(colander.Boolean())
    sidebar_categories_number = SidebarCategoriesNumber(colander.Integer())
    use_sidebar_archives = UseSidebarArchives(colander.Boolean())
    sidebar_archives_number = SidebarArchivesNumber(colander.Integer())


KottiBlogSidebarSettings = {
    'name': 'kotti_blog_sidebar_settings',
    'title': _(u'Blog sidebar settings'),
    'description': _(u"Settings for kotti_blog sidebar"),
    'success_message': _(u"Successfully saved blog sidebar settings."),
    'schema_factory': KottiBlogSidebarSettingsSchema,
}


def populate_settings():
    add_settings(KottiBlogSettings)
    add_settings(KottiBlogSidebarSettings)
    show_sidebar = get_setting('show_sidebar', False)
    if show_sidebar:
        slot = get_setting('slot', u'right')
        assign_slot('blog_sidebar', slot)

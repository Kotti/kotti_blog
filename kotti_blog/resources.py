import datetime
from datetime import date
from dateutil.tz import tzutc
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import types

from kotti.resources import Document
from kotti_blog import _


class UTCDateTime(types.TypeDecorator):
    impl = types.DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            return value.astimezone(tzutc())

    def process_result_value(self, value, engine):
        if value is not None:
            return datetime.datetime(value.year, value.month, value.day,
                    value.hour, value.minute, value.second, value.microsecond,
                    tzinfo=tzutc())


class Blog(Document):
    id = Column('id', Integer, ForeignKey('documents.id'), primary_key=True)

    type_info = Document.type_info.copy(
        name=u'Blog',
        title=_(u'Blog'),
        add_view=u'add_blog',
        addable_to=[u'Document'],
        )

    def get_unique_tags(self, request):
        children = self.children_with_permission(request)

        unique_tags_dict = {}
        for child in children:
            for tag in child.tags:
                try:
                    unique_tags_dict[tag] += 1
                except KeyError:
                    unique_tags_dict[tag] = 1

        return sorted(
            unique_tags_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )

    def get_archives(self, request):
        children = self.children_with_permission(request)

        dates_dict = {}
        for child in children:
            try:
                dates_dict[date(child.date.year, child.date.month, 1)] += 1
            except KeyError:
                dates_dict[date(child.date.year, child.date.month, 1)] = 1

        return sorted(dates_dict.items(), reverse=True)


class BlogEntry(Document):
    id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    date = Column('date', UTCDateTime())

    type_info = Document.type_info.copy(
        name=u'Blog entry',
        title=_(u'Blog entry'),
        add_view=u'add_blogentry',
        addable_to=[u'Blog'],
        )

    def __init__(self, date=None, **kwargs):
        super(BlogEntry, self).__init__(**kwargs)
        self.date = date

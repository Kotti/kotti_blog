import datetime
from dateutil.tz import tzutc
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    types,
)
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

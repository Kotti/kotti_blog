from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)
from kotti.resources import Document
from kotti_blog import _


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

    type_info = Document.type_info.copy(
        name=u'Blog entry',
        title=_(u'Blog entry'),
        add_view=u'add_blogentry',
        addable_to=[u'Blog'],
        )

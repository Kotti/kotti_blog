from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    UnicodeText,
)
from sqlalchemy.orm import mapper
from kotti import metadata
from kotti.resources import Document


class Blog(Document):
    type_info = Document.type_info.copy(
        name=u'Blog',
        add_view=u'add_blog',
        addable_to=[u'Document'],
        )

    # def __init__(self, body=u"", mime_type='text/html', **kwargs):
    #     super(Blog, self).__init__(**kwargs)
    #     self.body = body
    #     self.mime_type = mime_type


class BlogEntry(Document):
    type_info = Document.type_info.copy(
        name=u'Blog entry',
        add_view=u'add_blogentry',
        addable_to=[u'Blog'],
        )

blogs = Table('blogs', metadata,
    Column('id', Integer, ForeignKey('documents.id'), primary_key=True),
    Column('body', UnicodeText()),
)

blogentries = Table('blogentries', metadata,
    Column('id', Integer, ForeignKey('documents.id'), primary_key=True),
    Column('body', UnicodeText()),
)

mapper(Blog, blogs, inherits=Document, polymorphic_identity='blog')
mapper(BlogEntry, blogentries, inherits=Document, polymorphic_identity='blogentry')

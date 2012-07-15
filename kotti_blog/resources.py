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
    id = Column('id', Integer, ForeignKey('documents.id'), primary_key=True)
    body = Column('body', UnicodeText())

    type_info = Document.type_info.copy(
        name=u'Blog',
        title=u'Blog',
        add_view=u'add_blog',
        addable_to=[u'Document'],
        )

    # def __init__(self, body=u"", mime_type='text/html', **kwargs):
    #     super(Blog, self).__init__(**kwargs)
    #     self.body = body
    #     self.mime_type = mime_type


class BlogEntry(Document):
    id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    body = Column(UnicodeText())
    
    type_info = Document.type_info.copy(
        name=u'Blog entry',
        title=u'Blog entry',
        add_view=u'add_blogentry',
        addable_to=[u'Blog'],
        )

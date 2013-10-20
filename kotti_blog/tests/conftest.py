from pytest import fixture


@fixture
def kotti_blog_populate_settings(db_session):
    from kotti_blog.populate import populate_settings
    populate_settings()

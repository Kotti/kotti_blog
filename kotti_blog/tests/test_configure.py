from pyramid.interfaces import ITranslationDirectories

from kotti_blog import includeme
from kotti_blog import kotti_configure


def test_kotti_configure():

    settings = {
        'pyramid.includes': '',
        'kotti.available_types': '',
        'kotti.populators': '',
    }

    kotti_configure(settings)

    assert settings['pyramid.includes'] == ' kotti_blog kotti_blog.views kotti_blog.widgets'
    assert settings['kotti.available_types'] == \
        ' kotti_blog.resources.Blog kotti_blog.resources.BlogEntry'
    assert settings['kotti.populators'] == \
        ' kotti_blog.populate.populate_settings'


def test_includeme(config):

    includeme(config)

    utils = config.registry.__dict__['_utility_registrations']
    k = (ITranslationDirectories, u'')

    # test if the translation dir is registered
    assert k in utils
    assert utils[k][0][0].find('kotti_blog/locale') > 0

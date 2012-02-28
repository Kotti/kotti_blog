def kotti_configure(settings):
    settings['kotti.includes'] += 'kotti_blog.views'
    settings['kotti.available_types'] += ' kotti_blog.resources.Blog kotti_blog.resources.BlogEntry'

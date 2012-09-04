Blog addon for Kotti.

==========
kotti_blog
==========

This is an extension to the Kotti CMS that adds a simple blog system to your site.

`Find out more about Kotti`_

Setting up kotti_blog
=====================

This Addon adds two new Content Types to your Kotti site.
To set up the content types add ``kotti_blog.kotti_configure``
to the ``kotti.configurators`` setting in your ini file::

    kotti.configurators = kotti_blog.kotti_configure

Now you can create a blog and add blog entries to your blog.

There are different settings to adjust the behavior of the
blog.

You can select if the blog entries in the overview should
be batched. If you set ``kotti_blog.blog_settings.use_batching``
to ``true`` (the default value) the blog entries will be shown
on seperated pages. If you set it to ``false`` all blog entries
are shown all together on one page::

    kotti_blog.blog_settings.use_batching = false

If you use batching you can choose how many blog entries are
shown on one page. The default value for 
``kotti_blog.blog_settings.pagesize`` is 5::

    kotti_blog.blog_settings.pagesize = 10

You can use auto batching where the next page of the blog entries
is automatically loaded when scrolling down the overview page instead
of showing links to switch the pages. The default for
``kotti_blog.blog_settings.use_auto_batching`` is ``true``::

    kotti_blog.blog_settings.use_auto_batching = false

With ``kotti_blog.blog_settings.link_headline_overview`` you can control
wether the headline of a blog entry in the overview is linked to the blog 
entry or not. This setting defaults to ``true``::

    kotti_blog.blog_settings.link_headline_overview = false

Parts of kotti_blog can be overridden with the setting
``kotti_blog.asset_overrides``. Have a look to the 
`Kotti documentation about the asset_overrides setting`_, which is the same
as in ``kotti_blog``.

.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
.. _Kotti documentation about the asset_overrides setting: http://kotti.readthedocs.org/en/latest/configuration.html?highlight=asset#adjust-the-look-feel-kotti-asset-overrides

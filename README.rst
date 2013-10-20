Blog addon for Kotti.

==========
kotti_blog
==========

This is an extension to the Kotti CMS that adds a simple blog system to your site.

`Find out more about Kotti`_

Setting up kotti_blog
=====================

To activate the ``kotti_blog`` add-on in your Kotti site, you need to
add an entry to the ``kotti.configurators`` setting in your Paste
Deploy config.  ``kotti_blog`` depends on ``kotti_settings``, so you have to
add also an entry for this add-on::

    kotti.configurators =
        kotti_settings.kotti_configure
        kotti_blog.kotti_configure

``kotti_blog`` adds two new Content Types to your Kotti site.
Now you can create a blog and add blog entries to the blog.

There are different settings to adjust the behavior of the blog. Point
your browser to http://your.domain/@@settings to get to the settingspage
or use the submenupoint of 'Site Setup'.

You can select if the blog entries in the overview should
be batched. If activated the blog entries will be shown
on seperated pages. If not all blog entries are shown all together
on one page.

If you use batching you can choose how many blog entries are
shown on one page.

You can activate auto batching where the next page of the blog entries
is automatically loaded when scrolling down the overview page instead
of showing links to switch the pages.

With the last setting you can control wether the headline of a blog entry
in the overview is linked to the blog entry or not.

Parts of kotti_blog can be overridden with the setting
``kotti_blog.asset_overrides``. Have a look to the
`Kotti documentation about the asset_overrides setting`_, which is the same
as in ``kotti_blog``.

.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
.. _Kotti documentation about the asset_overrides setting: http://kotti.readthedocs.org/en/latest/configuration.html?highlight=asset#adjust-the-look-feel-kotti-asset-overrides

Changelog
*********

2.0.2 (2018-04-01)
==================

- make credentials and base url variables optional


2.0.1 (2018-01-03)
==================

- fix ``get_page_instance`` (missing page kwargs before page construction)


2.0.0 (2018-01-02)
==================

- navigation will no more be initialized automatically with an open
  browser by default since pypom_navigation is used by third party
  plugins even for non UI plugins. This way we avoid to open
  a browser if it is not needed and explicitly requested with a
  set page or visit page

- you can override the default page timeout using a ``pytest-variables``
  configuration named ``default_timeout``

- add new method ``get_page_instance`` on navigation


1.0.0 (2017-12-19)
==================

- navigation initialized with kwargs (including variables
  coming from pytest variables too)

- add global timeout for all pages (default 10)

- base_page fixture no longer opens page by default. It's up to you
  visiting a page now


0.1.1 (2017-10-30)
==================

- support fallback page classes in action_performed


0.1.0 (2017-10-12)
==================

- Add update_page and action_performed methods on navigation.
- Wait for pages to load when visiting them.


0.0.1 (2017-06-13)
==================

* First release


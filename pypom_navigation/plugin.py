# -*- coding: utf-8 -*-

import pytest

from .util import (
    get_page_class,
    page_factory,
)
from .navigation import Navigation


def pytest_addoption(parser):
    group = parser.getgroup('pypom-navigation')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2017',
        help='Set the value for the fixture "bar".'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo


@pytest.fixture(scope='session')
def skin():
    """ This fixture provides the skin associated with the application
        on which starts the test session.


        For example:

            @pytest.fixture(scope='session',
                            params=mypackage.DEFAULT_PAGES.keys())
            def skin(request):
                return request.param
    """
    return 'skin1'


@pytest.fixture(scope="session")
def default_pages():
    """ A mapping with the default page object class for each skin

        It's up to you override this fixture with your settings.

        For example::

            DEFAULT_PAGES = {
                'skin1': 'mypackage.pages.BasePage',
            }
    """
    return {'skin1': 'pypom_navigation.pages.BasePage'}


@pytest.fixture(scope="session")
def page_mappings():
    """
        Returns the page mappings that describes for each page id
        info like the page path, the page object class to be used
        or any other information::

            PAGE_MAPPINGS = {
                'HomePage': {'path': '/'},
                'LoginPage': {'path': '/'},
            }

        It's up to you override this fixture with your settings.

        :return: dictionary with all known pages
        :rtype: dict`
    """
    return {}


@pytest.fixture(scope='session')
def skin_base_url(skin, variables):
    """ Returns the skin_base_url associated to the skin.
    """
    return variables['skins'][skin]['base_url']


@pytest.fixture(scope='session')
def credentials_mapping(skin, variables):
    """
        This fixture provides users credentials via a file specified on the
        --variables option. The file format is one supported by
        pytest-variables.

        :return: credentials mapping dictionary with all available credentials
        :rtype: dict
        :raises: KeyError
    """
    return variables['skins'][skin]['credentials']


@pytest.fixture
def default_page_class(skin, page_mappings, default_pages):
    """
        Returns the default page object base class.

        :return: base page object class
        :rtype: :py:class:`tierra_qa.pages.BasePage`
    """
    return get_page_class(
        skin,
        page_mappings,
        default_pages=default_pages,
    )


@pytest.fixture
def base_page(skin_base_url, browser, default_page_class, page_mappings, skin):
    """ Base page instance """
    page = page_factory(
        skin_base_url,
        browser,
        default_page_class,
        page_mappings,
        skin)

    # visit target url
    page.open()

    return page


@pytest.fixture
def page_instance(base_page):
    """ Initialize base page.
        You can override this fixture in order to customize
        the page initialization (eg: some sites needs auth
        after, other sites before)
    """

    # maximize window
    base_page.driver.driver.maximize_window()

    return base_page


@pytest.fixture
def navigation(navigation_class,
               page_instance,
               default_page_class,
               page_mappings,
               credentials_mapping,
               skin,
               skin_base_url):
    """ Wraps a page and a page mappings accessible by
        pages.

        ``navigation.page`` is meant to be mutable since
        through the BDD steps the page instance could
        change.
    """
    nav = navigation_class(
        page_instance,
        default_page_class,
        page_mappings,
        credentials_mapping,
        skin,
        skin_base_url)
    return nav


@pytest.fixture
def navigation_class():
    """ Returns the navigation class used for wrap pages"""

    return Navigation


@pytest.fixture(autouse=True)
def skip_by_skin_names(request, skin):
    """ Skip by skin name.

        We support validation for multi skin applications providing the best
        page object class match.

        We expect many failures we want to avoid because many tests will fail
        because the related page object implementation still not exists.

        If you want you can omit a test execution for a given skin adding a
        a ```@pytest.mark.skip_skins(['skin2'])``` decorator on your tests.

        Tests marked with a skin2 skip will be executed for all skins
        except for skin2.

        See http://bit.ly/2dYnOSv for further info.
    """
    if request.node.get_marker('skip_skins'):
        if skin in request.node.get_marker('skip_skins').args[0]:
            pytest.skip('skipped on this skin: {}'.format(skin))

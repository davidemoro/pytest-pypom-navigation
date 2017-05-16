import pypom_navigation
import pypom_navigation.pages


def test_get_page_class1():
    """ page mapping without page_class"""
    from pypom_navigation.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {'path': '/'},
    }
    default_pages = {skin_name: 'pypom_navigation.pages.BasePage'}

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id,
        default_pages=default_pages) == pypom_navigation.pages.BasePage


def test_get_page_class2():
    """ page mapping with non matching skin, no fallback """
    from pypom_navigation.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {
            'path': '/',
            'page_class': {'skin2': 'pypom_navigation.pages'}
        },
    }
    default_pages = {skin_name: 'pypom_navigation.pages.BasePage'}

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id,
        default_pages=default_pages) == pypom_navigation.pages.BasePage


def test_get_page_class3():
    """ page mapping with non matching skin, with fallback """
    from pypom_navigation.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {
            'path': '/',
            'page_class': {
                'skin2': 'pypom_navigation.pages',
                'fallback': 'pypom_navigation',
            }
        },
    }
    default_pages = {skin_name: 'pypom_navigation.pages.BasePage'}

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id,
        default_pages=default_pages) == pypom_navigation


def test_get_page_class4():
    """ page mapping without non matching skin.
        Fallback in config ovverrides passed fallback.
    """
    from pypom_navigation.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {
            'path': '/',
            'page_class': {
                'skin2': 'pypom_navigation.pages',
                'fallback': 'pypom_navigation',
            }
        },
    }

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id,
        fallback=pypom_navigation.pages) == pypom_navigation


def test_get_page_class5():
    """ page mapping with non matching skin.
        Fallback in config wins against default page
        class (no fallback in conf)
    """
    from pypom_navigation.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {
            'path': '/',
            'page_class': {
                'skin2': 'pypom_navigation',
            }
        },
    }

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id,
        fallback=pypom_navigation.pages) == pypom_navigation.pages


def test_get_page_class6():
    """ page mapping with matching skin.
    """
    from pypom_navigation.util import get_page_class

    skin_name = 'skin1'
    page_id = 'HomePage'
    page_mappings = {
        'HomePage': {
            'path': '/',
            'page_class': {
                'skin1': 'pypom_navigation',
            }
        },
    }

    assert get_page_class(
        skin_name,
        page_mappings,
        page_id=page_id,
        fallback=pypom_navigation.pages) == pypom_navigation


def test_get_page_url_fallback():
    """ Test get page url fallback """
    from pypom_navigation.util import get_page_url

    assert get_page_url('skin1', {}, None) == '/'


def test_get_page_url_page_id():
    """ Test get page url page id """
    from pypom_navigation.util import get_page_url

    assert get_page_url('skin1', {'HelloPage': {}}, 'HelloPage') == '/'


def test_get_page_url_page_id_path():
    """ Test get page url page id path """
    from pypom_navigation.util import get_page_url

    assert get_page_url(
        'skin1',
        {'HelloPage': {'path': '/hello'}},
        'HelloPage') == '/hello'


def test_page_factory_1():
    """ Test page factory (page_id None) """
    import mock
    from pypom_navigation.util import page_factory

    page_mock = mock.Mock()

    page_id = None
    skin_name = 'skin1'
    base_url = 'http://baseurl.com'
    browser = None
    default_page_class = mock.Mock(return_value=page_mock)
    page_mappings = None

    result_page = page_factory(
        base_url,
        browser,
        default_page_class,
        page_mappings,
        skin_name,
        page_id=page_id)
    assert result_page is page_mock
    assert default_page_class.assert_called_once_with(
        browser,
        base_url=base_url
        ) is None


def test_page_factory():
    """ Test page factory (page_id not None) """
    import mock
    from pypom_navigation.util import page_factory

    page_mock = mock.Mock()

    page_id = 'pageID'
    skin_name = 'skin1'
    base_url = 'http://baseurl.com'
    browser = None
    default_page_class = mock.Mock(return_value=page_mock)
    page_mappings = {
        page_id: {
            'path': '/subpath',
            'page_class': {
                skin_name: 'mock.Mock'
            }
        }
    }

    result_page = page_factory(
        base_url,
        browser,
        default_page_class,
        page_mappings,
        skin_name,
        page_id=page_id)
    assert result_page is not page_mock
    assert not default_page_class.called
    assert result_page.base_url == 'http://baseurl.com/subpath'

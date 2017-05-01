import pytest
import pypom_navigation
import pypom_navigation.pages


@pytest.mark.parametrize("dotted,mod", [
    ('pypom_navigation.pages.BasePage', pypom_navigation.pages.BasePage,),
    ('pypom_navigation.pages.base.BasePage', pypom_navigation.pages.BasePage,),
    ('pypom_navigation', pypom_navigation,),
])
def test_dotted(dotted, mod):
    """ """
    from pypom_navigation.util import lookup_dotted_path

    assert lookup_dotted_path(
        dotted) == mod


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

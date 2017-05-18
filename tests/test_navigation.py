import pytest


@pytest.fixture
def page_instance():
    from mock import MagicMock
    return MagicMock()


@pytest.fixture
def skin_base_url():
    return 'https://skin1-coolsite.com'


@pytest.fixture
def credentials_mapping():
    return {
        'Administrator': {
            'username': 'admin',
            'password': 'pwd',
        }
    }


@pytest.fixture
def page_mappings():
    return {
        'HomePage': {
            'path': '/home',
        }
    }


@pytest.fixture
def default_page_class():
    from mock import MagicMock
    return lambda *args, **kwargs: MagicMock()


def test_navigation_init(
        navigation,
        page_instance,
        default_page_class,
        page_mappings,
        credentials_mapping,
        skin,
        skin_base_url):
    """ Navigation init """

    assert navigation.page == page_instance
    assert page_instance.navigation == navigation
    assert navigation.default_page_class == default_page_class
    assert navigation.page_mappings == page_mappings
    assert navigation.credentials_mapping == credentials_mapping
    assert navigation.skin == skin
    assert navigation.skin_base_url == skin_base_url
    assert navigation.page_id is None


def test_visit_page(navigation, page_instance):
    """ Test visit page """
    navigation.page == page_instance

    home_page = navigation.visit_page('HomePage')
    assert navigation.page is home_page
    assert navigation.page_id == 'HomePage'
    assert home_page.driver.visit.assert_called_once_with(
        'https://skin1-coolsite.com/home') is None


def test_get_credentials(navigation):
    """ Test get credentials """
    assert navigation.get_credentials('Administrator') == ('admin', 'pwd')

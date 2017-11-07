import pytest
from mock import MagicMock


@pytest.fixture
def variables():
    return {'foo': 'bar'}


@pytest.fixture
def page_instance():
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
            'path': '/home'
        },
        'AnotherPage': {
            'path': '/example',
            'actions': {'back': 'HomePage'}
        }
    }


@pytest.fixture
def default_page_class():
    return MagicMock()


def test_navigation_init(
        navigation,
        page_instance,
        default_page_class,
        page_mappings,
        credentials_mapping,
        skin,
        skin_base_url):
    """ Navigation init """

    assert navigation.page is page_instance
    assert page_instance.navigation is navigation
    assert navigation.default_page_class is default_page_class
    assert navigation.page_mappings == page_mappings
    assert navigation.credentials_mapping == credentials_mapping
    assert navigation.skin == skin
    assert navigation.skin_base_url == skin_base_url
    assert navigation.page_id is None


def test_visit_page(navigation, page_instance, default_page_class):
    """ Test visit page """
    home_page = navigation.visit_page('HomePage')
    assert navigation.page is home_page
    assert navigation.page_id == 'HomePage'
    assert home_page.driver.visit.assert_called_once_with(
        'https://skin1-coolsite.com/home') is None
    assert home_page.wait_for_page_to_load.assert_called_once() is None
    assert default_page_class.assert_called_once_with(
        page_instance.driver) is None
    assert default_page_class.return_value.navigation is navigation


def test_update_page(navigation, page_instance, default_page_class):
    """ Test update page """
    home_page = navigation.update_page('HomePage')
    assert navigation.page is home_page
    assert navigation.page_id == 'HomePage'
    assert home_page.wait_for_page_to_load.assert_called_once() is None
    assert default_page_class.assert_called_once_with(
        page_instance.driver) is None
    assert default_page_class.return_value.navigation is navigation


def test_action_performed(navigation, page_instance, default_page_class):
    """ Test visit page """
    navigation.setPage(page_instance, 'AnotherPage')
    home_page = navigation.action_performed('back')
    assert navigation.page is home_page
    assert navigation.page_id == 'HomePage'
    assert home_page.wait_for_page_to_load.assert_called_once() is None
    assert default_page_class.assert_called_once_with(
         page_instance.driver) is None
    assert default_page_class.return_value.navigation is navigation


def test_action_performed_no_action_mapped(navigation, page_instance,
                                           default_page_class):
    """ Test visit page """
    navigation.setPage(page_instance, 'AnotherPage')
    default_page = navigation.action_performed('unknown')
    assert navigation.page is default_page
    assert navigation.page_id is None
    assert default_page.wait_for_page_to_load.assert_called_once() is None
    assert default_page_class.assert_called_once_with(
        page_instance.driver) is None
    assert default_page_class.return_value.navigation is navigation


def test_action_performed_fallback(navigation, page_instance,
                                   default_page_class):
    """ Test visit page """
    navigation.setPage(page_instance, 'AnotherPage')
    fallback_class = MagicMock()
    fallback_page = navigation.action_performed('unknown',
                                                fallback=fallback_class)
    assert navigation.page is fallback_page
    assert navigation.page_id is None
    assert fallback_page.wait_for_page_to_load.assert_called_once() is None
    assert fallback_class.assert_called_once_with(page_instance.driver) is None
    assert fallback_class.return_value.navigation is navigation


def test_get_credentials(navigation):
    """ Test get credentials """
    assert navigation.get_credentials('Administrator') == ('admin', 'pwd')


def test_get_kwargs(navigation):
    """ Test kwargs """
    assert navigation.kwargs['variables']['foo'] == 'bar'

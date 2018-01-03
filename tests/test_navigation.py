import pytest
from mock import MagicMock


@pytest.fixture
def variables():
    return {'foo': 'bar'}


@pytest.fixture
def browser():
    return MagicMock()


@pytest.fixture
def page():
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
        default_page_class,
        page_mappings,
        credentials_mapping,
        skin,
        skin_base_url):
    """ Navigation init """

    assert navigation.page is None
    assert navigation.default_page_class is default_page_class
    assert navigation.page_mappings == page_mappings
    assert navigation.credentials_mapping == credentials_mapping
    assert navigation.skin == skin
    assert navigation.skin_base_url == skin_base_url
    assert navigation.page_id is None


def test_visit_page(navigation, default_page_class, browser,
                    default_timeout):
    """ Test visit page """
    home_page = navigation.visit_page('HomePage')
    assert navigation.page is home_page
    assert navigation.page_id == 'HomePage'
    assert home_page.driver.visit.assert_called_once_with(
        'https://skin1-coolsite.com/home') is None
    assert home_page.wait_for_page_to_load.assert_called_once() is None
    assert default_page_class.assert_called_once_with(
        browser, timeout=default_timeout) is None
    assert default_page_class.return_value.navigation is navigation


def test_update_page(navigation, default_page_class, browser,
                     default_timeout):
    """ Test update page """
    home_page = navigation.update_page('HomePage')
    assert navigation.page is home_page
    assert navigation.page_id == 'HomePage'
    assert home_page.wait_for_page_to_load.assert_called_once() is None
    assert default_page_class.assert_called_once_with(
        browser, timeout=default_timeout) is None
    assert default_page_class.return_value.navigation is navigation


def test_action_performed(navigation, page, default_page_class, browser,
                          default_timeout):
    """ Test visit page """
    navigation.setPage(page, 'AnotherPage')
    home_page = navigation.action_performed('back')
    assert navigation.page is home_page
    assert navigation.page_id == 'HomePage'
    assert home_page.wait_for_page_to_load.assert_called_once() is None
    assert default_page_class.assert_called_once_with(
         page.driver, timeout=default_timeout) is None
    assert default_page_class.return_value.navigation is navigation


def test_action_performed_no_action_mapped(navigation, page,
                                           default_page_class,
                                           default_timeout):
    """ Test visit page """
    navigation.setPage(page, 'AnotherPage')
    default_page = navigation.action_performed('unknown')
    assert navigation.page is default_page
    assert navigation.page_id is None
    assert default_page.wait_for_page_to_load.assert_called_once() is None
    assert default_page_class.assert_called_once_with(
        page.driver, timeout=default_timeout) is None
    assert default_page_class.return_value.navigation is navigation


def test_action_performed_fallback(navigation, page,
                                   default_page_class, default_timeout):
    """ Test visit page """
    navigation.setPage(page, 'AnotherPage')
    fallback_class = MagicMock()
    fallback_page = navigation.action_performed('unknown',
                                                fallback=fallback_class)
    assert navigation.page is fallback_page
    assert navigation.page_id is None
    assert fallback_page.wait_for_page_to_load.assert_called_once() is None
    assert fallback_class.assert_called_once_with(
        page.driver, timeout=default_timeout) is None
    assert fallback_class.return_value.navigation is navigation


def test_get_credentials(navigation):
    """ Test get credentials """
    assert navigation.get_credentials('Administrator') == ('admin', 'pwd')


def test_get_kwargs(navigation, default_timeout):
    """ Test kwargs """
    assert navigation.kwargs['timeout'] == default_timeout


def test_merge_kwargs(navigation, default_timeout):
    """ Test kwargs """
    assert navigation.kwargs['timeout'] == default_timeout
    assert 'new' not in navigation.kwargs
    merged = navigation.merge_kwargs(dict(new=1))
    assert merged['timeout'] == default_timeout
    assert merged['new'] == 1


def test_variables(navigation):
    """ Test kwargs """
    assert navigation.variables['foo'] == 'bar'


def test_get_page_instance(navigation, default_timeout,
                           default_page_class):
    """ Test kwargs """
    assert navigation.kwargs['timeout'] == default_timeout

    get_page_class = MagicMock(return_value=default_page_class)
    navigation.get_page_class = get_page_class
    assert navigation.get_page_class.called is False
    assert default_page_class.called is False
    navigation.get_page_instance()
    assert navigation.get_page_class.called is True
    assert navigation.get_page_class.called is True
    assert navigation.get_page_class.assert_called_once_with(
        fallback=None, page_id=None) is None
    assert default_page_class.assert_called_once_with(
        navigation.driver, timeout=default_timeout) is None


def test_get_page_instance_kwargs(navigation, default_timeout,
                                  default_page_class):
    """ Test kwargs """
    assert navigation.kwargs['timeout'] == default_timeout
    assert 'new' not in navigation.kwargs

    get_page_class = MagicMock(return_value=default_page_class)
    navigation.get_page_class = get_page_class
    assert navigation.get_page_class.called is False
    assert default_page_class.called is False
    navigation.get_page_instance(new=2)
    assert navigation.get_page_class.called is True
    assert navigation.get_page_class.called is True
    assert navigation.get_page_class.assert_called_once_with(
        fallback=None, page_id=None) is None
    assert default_page_class.assert_called_once_with(
        navigation.driver, timeout=default_timeout, new=2) is None
    assert navigation.kwargs['timeout'] == default_timeout
    assert 'new' not in navigation.kwargs

# -*- coding: utf-8 -*-

import pytest


def test_skin(skin):
    """ Skin fixture must return default value """
    assert skin == 'skin1'


def test_default_pages(default_pages, skin):
    """ Default pages fixture must return a valid mapping for default skin """
    assert default_pages[skin] == 'pypom_navigation.pages.BasePage'


def test_page_mappings(page_mappings):
    """ Empty page mappings by default """
    assert len(page_mappings.keys()) == 0


def test_default_page_class(default_page_class):
    """ Default page class """
    from pypom_navigation.pages import BasePage
    assert default_page_class is BasePage


def test_navigation_class(navigation_class):
    """ Default navigation class """
    from pypom_navigation.navigation import Navigation
    assert navigation_class is Navigation


@pytest.mark.parametrize('credentials_file', ['credentials.json',
                                              'credentials.yml'])
def test_credentials_mapping(testdir, credentials_file):
    """ Credentials available """
    import os

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_generated_credentials(credentials_mapping, skin, variables):
            assert variables['skins'][skin]['credentials']\
                ['Administrator']['username'] == "admin1"
            assert variables['skins'][skin]['credentials']\
                ['Administrator']['password'] == "asdf1"
            assert credentials_mapping['Administrator']['username'] == "admin1"
            assert credentials_mapping['Administrator']['password'] == "asdf1"
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--variables={0}'.format(os.path.join(os.path.dirname(__file__),
                                              credentials_file)),
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_generated_credentials PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


@pytest.mark.parametrize('credentials_file', ['credentials.json',
                                              'credentials.yml'])
def test_skin_base_url(testdir, credentials_file):
    """ Skin base url """
    import os

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_generated_skin_base_url_dummy(skin_base_url, skin, variables):
            assert variables['skins'][skin]\
                ['base_url'] == 'https://skin1-coolsite.com'
            assert skin_base_url == "https://skin1-coolsite.com"
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--variables={0}'.format(os.path.join(os.path.dirname(__file__),
                                              credentials_file)),
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_generated_skin_base_url_dummy PASSED',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


@pytest.mark.parametrize('credentials_file', ['credentials.yml',
                                              'credentials.json'])
def test_skin_base_url_multiple(testdir, credentials_file):
    """ Skin base url (multiple skins).
        You can run your tests multiple times for each supported skin.

        In this test we show how to override the default (single) skin
        fixture with a new multiple one with skin1 and skin2.

        skin1 and skin2 must be configured in credentials file.
    """
    import os

    # create a temporary pytest test module
    testdir.makepyfile("""
        import pytest


        @pytest.fixture(scope='session', params=['skin1', 'skin2'])
        def skin(request):
            return request.param


        def test_generated_skin_base_url_multiple(skin_base_url, skin,
                                                  variables):
            if skin == 'skin1':
                assert skin_base_url == 'https://skin1-coolsite.com'
            elif skin == 'skin2':
                assert skin_base_url == 'https://skin2-coolsite.com'
            assert variables['skins'][skin]\
                ['base_url'] == skin_base_url
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--variables={0}'.format(os.path.join(os.path.dirname(__file__),
                                              credentials_file)),
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result_text = result.stdout.str()
    assert 'test_generated_skin_base_url_multiple[skin1] PASSED' in result_text
    assert 'test_generated_skin_base_url_multiple[skin2] PASSED' in result_text

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


@pytest.mark.parametrize('credentials_file', ['credentials.yml',
                                              'credentials.json'])
def test_skip_by_skin_names(testdir, credentials_file):
    """ Skip by skin names
    """
    import os

    # create a temporary pytest test module
    testdir.makepyfile("""
        import pytest


        @pytest.fixture(scope='session', params=['skin1', 'skin2'])
        def skin(request):
            return request.param


        @pytest.mark.skip_skins(['skin1'])
        def test_generated_skip_skins(skin_base_url, skin,
                                      variables):
            if skin == 'skin1':
                assert 0
            elif skin == 'skin2':
                assert skin_base_url == 'https://skin2-coolsite.com'
            assert variables['skins'][skin]\
                ['base_url'] == skin_base_url
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--variables={0}'.format(os.path.join(os.path.dirname(__file__),
                                              credentials_file)),
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result_text = result.stdout.str()
    assert 'test_generated_skip_skins[skin1] SKIPPED' in result_text
    assert 'test_generated_skip_skins[skin2] PASSED' in result_text

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


@pytest.mark.parametrize('credentials_file', ['credentials.yml',
                                              'credentials.json'])
def test_skip_by_skin_names_import(testdir, credentials_file):
    """ Skip by skin names
    """
    import os

    # create a temporary pytest test module
    testdir.makepyfile("""
        import pytest
        from pypom_navigation.plugin import skip_skins


        @pytest.fixture(scope='session', params=['skin1', 'skin2'])
        def skin(request):
            return request.param


        @skip_skins(['skin1'])
        def test_generated_skip_skins(skin_base_url, skin,
                                      variables):
            if skin == 'skin1':
                assert 0
            elif skin == 'skin2':
                assert skin_base_url == 'https://skin2-coolsite.com'
            assert variables['skins'][skin]\
                ['base_url'] == skin_base_url
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--variables={0}'.format(os.path.join(os.path.dirname(__file__),
                                              credentials_file)),
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result_text = result.stdout.str()
    assert 'test_generated_skip_skins[skin1] SKIPPED' in result_text
    assert 'test_generated_skip_skins[skin2] PASSED' in result_text

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_base_page():
    from mock import patch
    from mock import Mock
    from pypom_navigation.plugin import base_page

    page_mock = Mock()

    with patch('pypom_navigation.plugin.page_factory') as page_factory:
        page_factory.return_value = page_mock

        skin_base_url = None
        browser = None
        default_page_class = None
        page_mappings = None
        skin = None
        base_page(skin_base_url, browser,
                  default_page_class, page_mappings, skin)
        assert page_factory.assert_called_once_with(
            skin_base_url,
            browser,
            default_page_class,
            page_mappings,
            skin) is None
        assert page_mock.open.called is True


def test_page_instance():
    """ page instance fixture customizes the base page (for example)
        by default maximize windows has called but you can override it
    """
    from mock import MagicMock
    from pypom_navigation.plugin import page_instance

    base_page = MagicMock()
    assert page_instance(base_page) is base_page

    assert base_page.driver.driver.maximize_window \
        .assert_called_once_with() is None


def test_navigation():
    """ Test navigation  """
    from mock import Mock
    from pypom_navigation.plugin import navigation

    navigation_instance = Mock()
    navigation_class = Mock()
    navigation_class.return_value = navigation_instance

    page_instance = object()
    default_page_class = object()
    page_mappings = object()
    credentials_mapping = object()
    skin = object()
    skin_base_url = object()

    assert navigation(
        navigation_class,
        page_instance,
        default_page_class,
        page_mappings,
        credentials_mapping,
        skin,
        skin_base_url,
        variables={},
    ) is navigation_instance
    assert navigation_class.assert_called_once_with(
        page_instance,
        default_page_class,
        page_mappings,
        credentials_mapping,
        skin, skin_base_url, variables={}) is None


def test_test_run_identifier(test_run_identifier, skin):
    """ Test run identifier """
    assert test_run_identifier.startswith('QA-')
    assert test_run_identifier.endswith('-{0}'.format(skin))


def test_now(now):
    """ Test now """
    assert now.isoformat()


def test_bdd_vars(bdd_vars, skin, now, test_run_identifier):
    """ Test bdd_vars """
    assert bdd_vars['skin'] == skin
    assert bdd_vars['datetime'] == now.isoformat()
    assert bdd_vars['test_run_identifier'] == test_run_identifier


def test_parametrizer_class(parametrizer_class):
    """ Test parametrizer class """
    from pypom_navigation.parametrizer import Parametrizer
    assert parametrizer_class is Parametrizer


def test_parametrizer(parametrizer_class, parametrizer, test_run_identifier):
    """ Test parametrizer """
    assert isinstance(parametrizer, parametrizer_class)
    assert parametrizer.parametrize(
        '$test_run_identifier') == test_run_identifier

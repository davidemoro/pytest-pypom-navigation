try:
    from urlparse import urljoin
except ImportError:
    # python3 compatibility
    from urllib.parse import urljoin

from .util import (
    get_page_class,
    get_page_url,
)


class Navigation(object):
    page_id = None

    def __init__(self,
                 page,
                 default_page_class,
                 page_mappings,
                 credentials_mapping,
                 skin,
                 skin_base_url,
                 **kwargs):
        self.setPage(page)
        self.default_page_class = default_page_class
        self.page_mappings = page_mappings
        self.credentials_mapping = credentials_mapping
        self.skin = skin
        self.skin_base_url = skin_base_url
        self.kwargs = kwargs

    def setPage(self, page, page_id=None):
        """ Set wrapping page and update reference links
            for page and navigation
        """
        page.navigation = self
        self.page = page
        self.page_id = page_id

    def visit_page(self, page_id, **kwargs):
        """ Visit page id reference in navigation
            class
        """
        page_url = urljoin(self.skin_base_url, self.get_page_url(page_id))
        page_instance = self._page_instance(page_id=page_id, **kwargs)
        page_instance.driver.visit(page_url)
        page_instance.wait_for_page_to_load()
        self.setPage(page_instance, page_id=page_id)
        return page_instance

    def update_page(self, page_id, **kwargs):
        """ Update the wrapped page with the appropriate instance
            mapped to the passed page_id
        """
        page_instance = self._page_instance(page_id=page_id, **kwargs)
        page_instance.wait_for_page_to_load()
        self.setPage(page_instance, page_id=page_id)
        return page_instance

    def action_performed(self, action, fallback=None, **kwargs):
        """ Update the wrapped page with the appropriate instance
            referenced by the given action on the current page
        """
        page_mapping = self.page_mappings[self.page_id]
        page_id = page_mapping.get('actions', {}).get(action)
        if page_id:
            return self.update_page(page_id, **kwargs)
        else:
            page_instance = self._page_instance(fallback=fallback, **kwargs)
            page_instance.wait_for_page_to_load()
            self.setPage(page_instance)
            return page_instance

    def get_page_url(self, page_id):
        """ Return the page url for the current wrapped page """
        return get_page_url(self.skin,
                            self.page_mappings, page_id)

    def get_credentials(self, user_id):
        """ Return a tuple with username and password for the given
            user_id
        """
        user_credentials = self.credentials_mapping[user_id]
        return user_credentials['username'], user_credentials['password']

    def get_page_class(self, page_id=None, fallback=None):
        """ Return the page class """
        fallback = fallback and fallback or self.default_page_class
        return get_page_class(
            self.skin,
            self.page_mappings,
            page_id=page_id,
            fallback=fallback)

    def _page_instance(self, page_id=None, fallback=None, **kwargs):
        page_class = self.get_page_class(page_id=page_id, fallback=fallback)
        return page_class(self.page.driver, **kwargs)

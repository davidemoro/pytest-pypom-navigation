from pypom_form.form import BaseFormPage


class BasePage(BaseFormPage):
    """ Base page """

    @property
    def current_url(self):
        """
            Returns the current url

            :return: current_url of the driver instance
            :rtype: str
        """
        return self.driver.url

    def wait_for_url_change(self, url):
        """
            Wait for url change occurred.

            :return: BasePage instance
            :rtype: object
        """
        self.wait.until(lambda s: self.current_url != url)
        return self

    def has_text(self, text):
        """
            Check for text in page.

            :return: True if the given text is present
            :rtype: bool
        """
        return self.driver.is_text_present(text, wait_time=self.timeout)

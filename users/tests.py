from selenium import webdriver
from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse


class SeleniumAuthTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_login_form(self):
        """Test login page for the presence of login form."""
        # To to login page.
        self.browser.get(self.live_server_url + reverse("django.contrib.auth.views.login"))
        # Check if login form is available.
        self.assertIn("Login", self.browser.find_element_by_class_name("form-horizontal").text)

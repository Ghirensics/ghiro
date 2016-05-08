from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.conf import settings

class LoginTest(LiveServerTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.browser.get(self.live_server_url + reverse("django.contrib.auth.views.login"))
        self.browser.find_element_by_id("id_username").send_keys("a")
        self.browser.find_element_by_id("id_password").send_keys("a" + Keys.RETURN)

    def test_release_in_login_footer(self):
        self.browser.get(
            self.live_server_url + reverse("django.contrib.auth.views.login"))
        self.assertIn(settings.GHIRO_VERSION,
                      self.browser.find_element_by_tag_name("footer").text)
    
    def test_login_form_available(self):
         """Test login page for the presence of login form."""
         # To to login page.
         self.browser.get(self.live_server_url + reverse("django.contrib.auth.views.login"))
         # Check if login form is available.
         self.assertIn("Login", self.browser.find_element_by_class_name("form-horizontal").text)

    def test_login_ko_hit_return(self):
         test_creds = [("", ""), ("a", ""), ("", "a"), ("a", "a")]
         for user, passwd in test_creds:
             self.browser.get(self.live_server_url + reverse("django.contrib.auth.views.login"))
             self.browser.find_element_by_id("id_username").send_keys(user)
             self.browser.find_element_by_id("id_password").send_keys(passwd + Keys.RETURN)
             self.assertTrue(self.browser.find_element_by_id("failed-login-alert").is_displayed())

    def test_login_ko_hit_return(self):
         test_creds = [("", ""), ("a", ""), ("", "a"), ("a", "a")]
         for user, passwd in test_creds:
             self.browser.get(
                self.live_server_url + reverse(
                    "django.contrib.auth.views.login"))
             self.browser.find_element_by_id("id_username").send_keys(user)
             self.browser.find_element_by_id("id_password").send_keys(passwd)
             self.browser.find_element_by_xpath("//*[@id='upper']/form/div[3]/div/button").click()
             self.assertTrue(self.browser.find_element_by_id(
                 "failed-login-alert").is_displayed())
#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from base import Base


class LoginPage(Base):
    # TODO: This obviously should change. File bug
    _page_title = "CloudForms Management Engine: Dashboard"
    _login_username_field_locator = (By.CSS_SELECTOR, '#user_name')
    _login_password_field_locator = (By.CSS_SELECTOR, '#user_password')
    _login_submit_button_locator = (By.ID, 'login')

    @property
    def is_the_current_page(self):
        '''Override the base implementation to make sure that we are actually on the login screen
        and not the actual dashboard
        '''
        return Base.is_the_current_page and \
            self.is_element_visible(*self._login_submit_button_locator)

    @property
    def username(self):
        return self.selenium.find_element(*self._login_username_field_locator)

    @property
    def password(self):
        return self.selenium.find_element(*self._login_password_field_locator)

    @property
    def login_button(self):
        return self.selenium.find_element(*self._login_submit_button_locator)

    def _click_on_login_button(self):
        self.login_button.click()

    def _press_enter_on_login_button(self):
        self.login_button.send_keys(Keys.RETURN)

    def _click_on_login_and_send_window_size(self):
        self.login_button.click()
        driver = self.login_button.parent
        driver.execute_script("""miqResetSizeTimer();""")

    def login(self, *args, **kwargs):
        return self.login_with_mouse_click(*args, **kwargs)

    def login_with_enter_key(self, *args, **kwargs):
        return self._do_login(self._press_enter_on_login_button, *args, **kwargs)

    def login_with_mouse_click(self, *args, **kwargs):
        return self._do_login(self._click_on_login_button, *args, **kwargs)

    def login_and_send_window_size(self, *args, **kwargs):
        return self._do_login(self._click_on_login_and_send_window_size, *args, **kwargs)

    def _do_login(self, continue_function, user='default', force_dashboard=True):
        self._set_login_fields(user)
        # TODO: Remove once bug is fixed
        time.sleep(1.25)
        continue_function()
        try:
            self._wait_for_results_refresh()
        except:
            self._wait_for_results_refresh()

        from pages.dashboard import DashboardPage
        page = DashboardPage(self.testsetup)
        try:
            page.is_the_current_page
        except AssertionError:
            if force_dashboard:
                from fixtures.navigation import intel_dashboard_pg
                page = intel_dashboard_pg()
            else:
                # Not the dashboard page and not forcing dashboard page
                # return a generic Base page
                page = Base(self.testsetup)
        return page

    def _set_login_fields(self, user='default'):
        credentials = self.testsetup.credentials[user]
        self.username.send_keys(credentials['username'])
        self.password.send_keys(credentials['password'])

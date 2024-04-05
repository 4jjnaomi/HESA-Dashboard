"""
This file is used to configure the pytest framework.
"""

import os
import pytest

from dash.testing.application_runners import import_app

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def pytest_setup_options():
    """pytest extra command line arguments for running chrome driver

     For GitHub Actions or similar container you need to run it headless.
     When writing the tests and running locally it may be useful to
     see the browser and so you need to see the browser.
    """
    options = Options()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("--start-maximized")
    return options


@pytest.fixture
def dash_app():
    """Fixture to create a Dash app instance."""
    app = import_app(app_file='app')
    return app


@pytest.fixture
def start_dash_app(dash_duo, dash_app):
    """Fixture to start the Dash app."""
    dash_duo.start_server(dash_app)


@pytest.fixture
def wait_for_element(dash_duo):
    """Fixture to wait for an element to be present on the page."""
    def _wait_for_element(selector, timeout=30):
        return WebDriverWait(dash_duo.driver, timeout).until(
            EC.presence_of_element_located(selector)
        )
    return _wait_for_element


@pytest.fixture
def navigate_to_page(start_dash_app, dash_duo):
    """Fixture to navigate to a specific page."""
    def _navigate_to_page(page_url):
        dash_duo.driver.get(dash_duo.server_url + page_url)
    return _navigate_to_page


@pytest.fixture
def click_element(dash_duo):
    """Fixture to find and click a dropdown element."""
    def _click_element(dropdown_id):
        # Get the element
        element = dash_duo.driver.find_element(By.ID, dropdown_id)
        # Click the element
        element.click()

    return _click_element


@pytest.fixture
def choose_select_dbc_option(dash_duo, wait_for_element):
    """Fixture to choose an option in a DBC Select component."""
    def _choose_select_dbc_option(select_id, option_value):
        # Wait for the select component to be clickable
        wait_for_element((By.ID, select_id))
        # Find the select component
        select = dash_duo.driver.find_element(By.ID, select_id)
        # Initialize Select object for the select component
        select_object = Select(select)
        # Select the option with the specified value
        select_object.select_by_value(option_value)
    return _choose_select_dbc_option

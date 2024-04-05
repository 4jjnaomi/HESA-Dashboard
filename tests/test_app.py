"""
This module contains test cases for the Dash app.

The test cases include:
- Checking if the server is live and responding with a 200 status code.
- Testing the navigation functionality of the navbar links.
- Verifying that the app displays a 404 Page Not Found message for non-existing pages.
"""

import time
import requests
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_server_live(dash_duo, dash_app, start_dash_app):
    """
    GIVEN the Dash app is running
    WHEN a HTTP request to the home page is made
    THEN the server should respond with a 200 status code
    """

    # Wait for the page to load
    time.sleep(2)

    # Get the URL
    url = dash_duo.driver.current_url

    # Make a HTTP request to the home page
    response = requests.get(url, timeout=5)

    # Assert the server responds with a 200 status code
    assert response.status_code == 200


@pytest.mark.parametrize("link_index, expected_url", [(0, '/'), (1, '/ranking_table'), (2, '/comparison')])
def test_navbar_links(dash_duo, navigate_to_page, wait_for_element, link_index, expected_url):
    """
    GIVEN the Dash app is running
    WHEN a user clicks on a link in the navbar
    THEN the app should navigate to the corresponding page
    """

    navigate_to_page('/')

    # Wait for the navbar to load
    wait_for_element((By.CLASS_NAME, 'navbar'))

    # Get the navbar
    navbar = dash_duo.driver.find_element(By.CLASS_NAME, 'navbar')

    # Get the links in the navbar
    links = navbar.find_elements(By.TAG_NAME, 'a')

    # Click on the link in the navbar
    links[link_index].click()

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.url_to_be(dash_duo.server_url + expected_url))

    # Assert that the URL has changed to the correct page
    assert dash_duo.driver.current_url == dash_duo.server_url + expected_url


def test_404_page(dash_duo, navigate_to_page, wait_for_element):
    """
    GIVEN the Dash app is running
    WHEN a user navigates to a non-existing page
    THEN the app should display a 404 Page Not Found message
    """

    # Navigate to a non-existing page
    navigate_to_page('/non_existing_page')

    # Wait for the 404 message to appear
    wait_for_element((By.TAG_NAME, "h1"))

    # Get the text of the h1 element
    h1_text = dash_duo.driver.find_element(By.TAG_NAME, "h1").text

    # Assert that the h1 element contains the expected text
    assert "404 - Page not found" in h1_text

import time
import requests
import pytest
from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_server_live(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN a HTTP request to the home page is made
    THEN the server should respond with a 200 status code
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Wait for the page to load
    time.sleep(2)

    #Get the url
    url = dash_duo.driver.current_url

    #Make a HTTP request to the home page
    response = requests.get(url)

    # Assert the server responds with a 200 status code
    assert response.status_code == 200

@pytest.mark.parametrize("link_index, expected_url", [(1, '/map_view'), (2, '/ranking_table')])
def test_navbar_links(dash_duo, link_index, expected_url):
    """
    GIVEN the Dash app is running
    WHEN a user clicks on a link in the navbar
    THEN the app should navigate to the corresponding page
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Get the navbar
    navbar = dash_duo.driver.find_element(By.CLASS_NAME, 'navbar')

    # Get the links in the navbar
    links = navbar.find_elements(By.TAG_NAME, 'a')

    # Click on the link in the navbar
    links[link_index].click()

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(EC.url_to_be(dash_duo.server_url + expected_url))

    # Assert that the URL has changed to the correct page
    assert dash_duo.driver.current_url == dash_duo.server_url + expected_url

def test_404_page(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN a user navigates to a non-existing page
    THEN the app should display a 404 Page Not Found message
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to a non-existing page
    dash_duo.driver.get(dash_duo.server_url + '/non_existing_page')

    # Wait for the 404 message to appear
    WebDriverWait(dash_duo.driver, 30).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h1"))
    )

    # Get the text of the h1 element
    h1_text = dash_duo.driver.find_element(By.TAG_NAME, "h1").text

    # Assert that the h1 element contains the expected text
    assert "404 - Page not found" in h1_text

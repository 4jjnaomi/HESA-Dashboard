import time
import requests
from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By

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
    url = dash_duo.current_url

    #Make a HTTP request to the home page
    response = requests.get(url)

    # Assert the server responds with a 200 status code
    assert response.status_code == 200
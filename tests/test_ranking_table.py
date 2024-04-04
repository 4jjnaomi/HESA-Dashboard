from dash.testing.application_runners import import_app

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def test_ranking_table_layout(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user navigates to the ranking table page
    THEN the layout should contain the expected components
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the ranking table page
    dash_duo.driver.get(dash_duo.server_url + '/ranking_table')

    # Wait for the table to load
    WebDriverWait(dash_duo.driver, 10).until(
        EC.presence_of_element_located((By.ID, "ranking-table"))
    )

    # Get the layout elements
    class_dropdown = dash_duo.find_element("#class-dropdown-rank")
    year_dropdown = dash_duo.find_element("#year-dropdown-rank")
    table_div = dash_duo.find_element("#ranking-table")

    # Assert that the layout contains the expected components
    assert class_dropdown.is_displayed()
    assert year_dropdown.is_displayed()
    assert table_div.is_displayed()

def test_ranking_table_callback(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user selects options in the dropdowns
    THEN the table should update accordingly
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the ranking table page
    dash_duo.driver.get(dash_duo.server_url + '/ranking_table')

    # Wait for the table to load
    WebDriverWait(dash_duo.driver, 10).until(
        EC.presence_of_element_located((By.ID, "ranking-table"))
    )

    # Get the initial table content
    initial_table_content = dash_duo.find_element("#ranking-table").text

    # Find the class dropdown element
    class_dropdown_element = dash_duo.driver.find_element(By.ID, "class-dropdown-rank")
    # Initialize Select object for the class dropdown
    class_dropdown = Select(class_dropdown_element)

    # Select the option with value "Finances and people"
    class_dropdown.select_by_value("Finances and people")

    # Wait for the table content to change
    WebDriverWait(dash_duo.driver, 10).until(
        lambda driver: dash_duo.find_element("#ranking-table").text != initial_table_content
    )

    # Get the updated table content
    updated_table_content = dash_duo.find_element("#ranking-table").text

    # Assert that the table content has been updated
    assert updated_table_content != initial_table_content

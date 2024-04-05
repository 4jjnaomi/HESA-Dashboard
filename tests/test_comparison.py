"""
This module contains tests for the comparison page of the Dash app.

The tests include:
- Checking if the comparison page contains the expected components.
- Testing if selecting options in the dropdowns updates the bar chart.
- Testing if the category marker dropdown options remain 
unchanged when the class dropdown has no value selected.
"""

import time
from dash.testing.application_runners import import_app

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def test_comparison_page_layout(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user navigates to the comparison page
    THEN the layout should contain the expected components
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the comparison page
    dash_duo.driver.get(dash_duo.server_url + '/comparison')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.ID, "bar_chart"))
    )

    # Get the layout elements
    year_dropdown = dash_duo.driver.find_element(
        By.ID, "year-dropdown-comparison")
    class_dropdown = dash_duo.driver.find_element(
        By.ID, "class-dropdown-comparison")
    category_marker_dropdown = dash_duo.driver.find_element(
        By.ID, "category-marker-dropdown-comparison")
    category_dropdown = dash_duo.driver.find_element(
        By.ID, "category-dropdown-comparison")
    hei_dropdown = dash_duo.driver.find_element(
        By.ID, "hei-dropdown-comparison")

    # Assert that the layout contains the expected components
    assert year_dropdown.is_displayed()
    assert class_dropdown.is_displayed()
    assert category_marker_dropdown.is_displayed()
    assert category_dropdown.is_displayed()
    assert hei_dropdown.is_displayed()


def test_comparison_page_callback(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user selects options in the dropdowns
    THEN the bar chart should update accordingly
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the comparison page
    dash_duo.driver.get(dash_duo.server_url + '/comparison')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.ID, "bar_chart"))
    )

    # Click the year dropdown element
    year_dropdown_element = dash_duo.driver.find_element(
        By.ID, "year-dropdown-comparison")
    year_dropdown_element.click()

    # Find the year dropdown menu
    year_dropdown_menu = dash_duo.driver.find_element(
        By.CLASS_NAME, "Select-menu-outer")
    # Click the first option in the dropdown
    ActionChains(dash_duo.driver).click(year_dropdown_menu).perform()

    # Get the class dropdown element
    class_dropdown_element = dash_duo.driver.find_element(
        By.ID, "class-dropdown-comparison")

    # Initialize Select object for the class dropdown
    class_dropdown = Select(class_dropdown_element)

    # Select the option with value "Building and spaces"
    class_dropdown.select_by_value("Building and spaces")

    # Get the category marker dropdown element
    category_marker_dropdown_element = dash_duo.driver.find_element(
        By.ID, "category-marker-dropdown-comparison")

    # Initialize Select object for the category marker dropdown
    category_marker_dropdown = Select(category_marker_dropdown_element)

    # Select the option with value "Grounds area"
    category_marker_dropdown.select_by_value("Grounds area")

    # Get the category dropdown element
    category_dropdown_element = dash_duo.driver.find_element(
        By.ID, "category-dropdown-comparison")

    # Initialize Select object for the category dropdown
    category_dropdown = Select(category_dropdown_element)

    # Select the option with value "Water (hectares)"
    category_dropdown.select_by_value("Water (hectares)")

    # Click the HEI dropdown element
    hei_dropdown_element = dash_duo.driver.find_element(
        By.ID, "hei-dropdown-comparison")
    hei_dropdown_element.click()

    # Find the hei dropdown menu
    hei_dropdown_menu = dash_duo.driver.find_element(
        By.CLASS_NAME, "Select-menu-outer")
    # Click the first option in the dropdown
    ActionChains(dash_duo.driver).click(hei_dropdown_menu).perform()

    time.sleep(3)

    # Get the initial bar chart content
    initial_bar_chart_content = dash_duo.find_element("#bar_chart").text

    # Enter another option in the HEI dropdown
    hei_dropdown_element.click()
    hei_dropdown_menu = dash_duo.driver.find_element(
        By.CLASS_NAME, "Select-menu-outer")
    ActionChains(dash_duo.driver).click(hei_dropdown_menu).perform()

    time.sleep(2)

    # Get the updated bar chart content
    updated_bar_chart_content = dash_duo.find_element("#bar_chart").text

    # Assert that the bar chart content has been updated
    assert updated_bar_chart_content != initial_bar_chart_content


def test_comparison_update_category_marker_no_class(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user navigates to the comparison page
    AND the class dropdown has no value selected
    THEN the category marker dropdown options should not change
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the comparison page
    dash_duo.driver.get(dash_duo.server_url + '/comparison')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located(
            (By.ID, "category-marker-dropdown-comparison"))
    )

    # Initialise the Select object for the category marker dropdown
    category_marker_dropdown_element = dash_duo.driver.find_element(
        By.ID, "category-marker-dropdown-comparison")
    category_marker_dropdown = Select(category_marker_dropdown_element)

    # Get the initial state of the category marker dropdown options
    initial_options = [
        option.text for option in category_marker_dropdown.options]

    # Simulate not selecting any option from the class dropdown to trigger the callback
    class_dropdown_element = dash_duo.driver.find_element(
        By.ID, "class-dropdown-comparison")
    class_dropdown = Select(class_dropdown_element)
    class_dropdown.select_by_value("")

    # Get the updated state of the category marker dropdown options
    updated_options = [
        option.text for option in category_marker_dropdown.options]

    # Assert that options remain unchanged
    assert initial_options == updated_options

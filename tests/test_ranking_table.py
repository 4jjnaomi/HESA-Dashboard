"""
This module contains tests for the ranking table page.

The tests include:
- Checking if the ranking table page contains the expected components.
- Testing if selecting options in the dropdowns updates the table.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def test_ranking_table_layout(dash_duo, navigate_to_page, wait_for_element):
    """
    GIVEN the Dash app is running
    WHEN the user navigates to the ranking table page
    THEN the layout should contain the expected components
    """

    navigate_to_page('/ranking_table')
    wait_for_element((By.ID, "ranking-table"))

    # Get the layout elements
    class_dropdown = dash_duo.find_element("#class-dropdown-rank")
    year_dropdown = dash_duo.find_element("#year-dropdown-rank")
    table_div = dash_duo.find_element("#ranking-table")

    # Assert that the layout contains the expected components
    assert class_dropdown.is_displayed()
    assert year_dropdown.is_displayed()
    assert table_div.is_displayed()


def test_ranking_table_callback(dash_duo, navigate_to_page, wait_for_element, choose_select_dbc_option):
    """
    GIVEN the Dash app is running
    WHEN the user selects options in the dropdowns
    THEN the table should update accordingly
    """

    navigate_to_page('/ranking_table')
    wait_for_element((By.ID, "ranking-table"))

    # Get the initial table content
    initial_table_content = dash_duo.find_element("#ranking-table").text

    choose_select_dbc_option("class-dropdown-rank", "Finances and people")

    # Wait for the table content to change
    WebDriverWait(dash_duo.driver, 10).until(
        lambda driver: dash_duo.find_element(
            "#ranking-table").text != initial_table_content
    )

    # Get the updated table content
    updated_table_content = dash_duo.find_element("#ranking-table").text

    # Assert that the table content has been updated
    assert updated_table_content != initial_table_content

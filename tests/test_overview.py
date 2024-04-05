"""
This module contains tests for the overview page of the Dash app.

The tests include:
- Checking if the overview page layout contains the expected components.
- Testing if selecting a category marker from the dropdown updates the line chart.
- Testing if clicking on the toggle button expands and collapses the sidebar.
- Testing if entering a search term in the sidebar search input filters the universities displayed.
- Testing if clicking on a university link in the sidebar 
navigates to the overview page of the selected university.
- Testing if navigating to the overview page of a non-existent 
university displays a message that the university was not found.
- Testing if the category marker dropdown options and value 
remain unchanged when the class dropdown has no value selected.
"""

from dash.testing.application_runners import import_app

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def test_overview_page_layout(dash_duo, navigate_to_page, wait_for_element):
    """
    GIVEN the Dash app is running
    WHEN the user navigates to the overview page
    THEN the layout should contain the expected components
    """

    # Navigate to the overview page
    navigate_to_page('/university/University College London')

    # Wait for the page to load
    wait_for_element((By.ID, "overview_line_chart"))

    # Get the layout elements
    class_dropdown = dash_duo.driver.find_element(By.ID, "class-dropdown")
    category_marker_dropdown = dash_duo.driver.find_element(
        By.ID, "category-marker-dropdown")
    toggle_button = dash_duo.driver.find_element(By.ID, "toggle")

    # Assert that the layout contains the expected components
    assert class_dropdown.is_displayed()
    assert category_marker_dropdown.is_displayed()
    assert toggle_button.is_displayed()


def test_overview_update_line_chart(dash_duo, navigate_to_page, wait_for_element, choose_select_dbc_option):
    """
    GIVEN the Dash app is running
    WHEN the user goes to the overview page of University College London
    AND selects a category marker from the dropdown
    THEN the line chart should update accordingly
    """

    # Navigate to the overview page
    navigate_to_page('/university/University College London')

    # Wait for the page to load
    wait_for_element((By.ID, "overview_line_chart"))

    # Get the initial line chart content
    initial_line_chart_content = dash_duo.find_element(
        "#overview_line_chart").text

    # Select the option with value "Building and spaces" from the class dropdown
    choose_select_dbc_option("class-dropdown", "Building and spaces")

    # Select the option with value 'Grounds area' from the category marker dropdown
    choose_select_dbc_option("category-marker-dropdown", "Grounds area")

    # Wait for the line chart content to change
    WebDriverWait(dash_duo.driver, 30).until(
        lambda driver: dash_duo.find_element(
            "#overview_line_chart").text != initial_line_chart_content
    )

    # Get the updated line chart content
    updated_line_chart_content = dash_duo.find_element(
        "#overview_line_chart").text

    # Assert that the line chart content has been updated
    assert updated_line_chart_content != initial_line_chart_content


def test_toggle_sidebar_button(dash_duo, navigate_to_page, wait_for_element, click_element):
    """
    GIVEN the Dash app is running
    WHEN the user goes to the overview page of University College London
    AND clicks on the toggle sidebar button
    THEN the sidebar should expand accordingly
    """

    navigate_to_page('/university/University College London')
    wait_for_element((By.ID, "collapse"))

    # Click on the toggle button
    click_element("toggle")

    # Wait for the sidebar to expand
    WebDriverWait(dash_duo.driver, 30).until(
        EC.visibility_of_element_located((By.ID, "collapse"))
    )

    # Get the updated state of the sidebar
    updated_sidebar_state = dash_duo.find_element(
        "#collapse").get_attribute("class")

    # Assert that the sidebar has expanded
    assert "show" in updated_sidebar_state

    # Click on the toggle button again
    click_element("toggle")

    # Wait for the sidebar to collapse
    WebDriverWait(dash_duo.driver, 30).until(
        EC.invisibility_of_element_located((By.ID, "collapse"))

    )
    # Get the updated state of the sidebar
    updated_sidebar_state = dash_duo.find_element(
        "#collapse").get_attribute("class")

    # Assert that the sidebar has collapsed
    assert "show" not in updated_sidebar_state


def test_sidebar_search(dash_duo, navigate_to_page, wait_for_element, click_element):
    """
    GIVEN the Dash app is running
    WHEN the user goes to the overview page of University College London
    AND clicks on the toggle sidebar button
    AND enters a search term in the sidebar search input
    THEN the sidebar should display only the universities that match the search term
    """
    navigate_to_page('/university/University College London')
    wait_for_element((By.ID, "collapse"))

    # Click on the toggle button
    click_element("toggle")

    # Wait for the search input element to be visible
    WebDriverWait(dash_duo.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "search_input"))
    )

    # Get the search input element
    search_input = dash_duo.find_element("#search_input")

    # Enter a search term in the search input
    search_input.send_keys("Bath")

    # Wait for the sidebar to update
    WebDriverWait(dash_duo.driver, 30).until(
        lambda driver: len(dash_duo.find_elements(".sidebar-nav-link")) < 5
    )

    # Check that the universities displayed in the sidebar are the ones that match the search term
    nav_links = dash_duo.find_elements(".sidebar-nav-link")
    for nav_link in nav_links:
        assert "Bath" in nav_link.text, f"Expected 'Bath' in nav link text, but got: {
            nav_link.text}"


def test_sidebar_link(dash_duo, navigate_to_page, wait_for_element, click_element):
    """
    GIVEN the Dash app is running
    WHEN the user goes to the overview page of University College London
    AND clicks on a university link in the sidebar
    THEN the page should navigate to the overview page of the selected university
    """
    navigate_to_page('/university/University College London')
    wait_for_element((By.ID, "collapse"))

    # Click on the toggle button
    click_element("toggle")

    WebDriverWait(dash_duo.driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "#sidebar-nav > a:nth-child(1)"))
    )

    # Get the first university link in the sidebar
    university_link = dash_duo.find_element("#sidebar-nav > a:nth-child(1)")

    # Get the text of the university link
    university_name = university_link.text

    # Click on the university link
    university_link.click()

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.url_contains('/university/')
    )

    # Assert that the URL has changed to the university overview page
    assert f'/university/{university_name}' in dash_duo.driver.current_url


def test_non_existent_university_overview(dash_duo, navigate_to_page, wait_for_element):
    """
    GIVEN the Dash app is running
    WHEN the user goes to the overview page of a non-existent university
    THEN the app should display a message that the university was not found
    """

    # Navigate to a non-existent university overview page
    navigate_to_page('/university/NonExistentUniversity')
    wait_for_element((By.TAG_NAME, "h1"))

    # Get the text of the h1 element
    h1_text = dash_duo.driver.find_element(By.TAG_NAME, "h1").text

    # Assert that the h1 element contains the expected text
    assert "University not found" in h1_text


def test_update_category_marker_dropdown_no_class_name(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the class dropdown has no value selected
    THEN the category marker dropdown options should not change
    AND the category marker dropdown value should remain None
    """
    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the overview page
    dash_duo.driver.get(dash_duo.server_url +
                        '/university/University College London')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.ID, "category-marker-dropdown"))
    )

    # Initialise the Select object for the category marker dropdown
    category_marker_dropdown_element = dash_duo.driver.find_element(
        By.ID, "category-marker-dropdown")
    category_marker_dropdown = Select(category_marker_dropdown_element)

    # Get the initial state of the category marker dropdown options and value
    initial_options = [
        option.text for option in category_marker_dropdown.options]
    initial_value = category_marker_dropdown.first_selected_option.text

    # Simulate not selecting any option from the class dropdown to trigger the callback
    class_dropdown_element = dash_duo.driver.find_element(
        By.ID, "class-dropdown")
    class_dropdown = Select(class_dropdown_element)
    class_dropdown.select_by_value("")

    # Get the updated state of the category marker dropdown options and value
    updated_options = [
        option.text for option in category_marker_dropdown.options]
    updated_value = category_marker_dropdown.first_selected_option.text

    # Assert that options and value remain unchanged
    assert initial_options == updated_options
    assert initial_value == updated_value

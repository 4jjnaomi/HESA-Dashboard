import time
import requests
import pytest
from dash.testing.application_runners import import_app

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
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
    response = requests.get(url, timeout=5)

    # Assert the server responds with a 200 status code
    assert response.status_code == 200

@pytest.mark.parametrize("link_index, expected_url", [(0,'/'), (1, '/ranking_table'), (2, '/comparison')])
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

def test_homepage_content(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN a user navigates to the home page
    THEN the app should display the home page content
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the home page
    dash_duo.driver.get(dash_duo.server_url + '/')

    # Wait for the page to load
    # Wait for the map to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "geolayer"))
    )

    # Get the layout elements
    heading = dash_duo.driver.find_element(By.TAG_NAME, "h1")
    buttons = dash_duo.driver.find_elements(By.CLASS_NAME, "btn")
    region_dropdown = dash_duo.driver.find_element(By.ID, "region-dropdown-map")
    hei_dropdown = dash_duo.driver.find_element(By.ID, "hei-dropdown-map")
    card_div = dash_duo.driver.find_element(By.ID, "card")

    # Assert that the layout contains the expected components
    assert heading.is_displayed()
    assert len(buttons) == 3
    assert region_dropdown.is_displayed()
    assert hei_dropdown.is_displayed()
    assert not card_div.is_displayed()

def test_map_marker_select_updates_card(dash_duo):
    """
    GIVEN the app is running which has a <div id='map'>
    THEN there should not be any elements with a class of 'card' on the page
    WHEN a marker in the map is hovered over
    THEN there should be one more card on the page than there was at the start
    AND there should be a text value for the h6 heading in the card
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Wait for the map to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#england_map > div.js-plotly-plot > div > div > svg:nth-child(5)"))
    )

    # Get the initial number of cards
    initial_num_cards = len(dash_duo.driver.find_elements(By.CLASS_NAME, "card-body"))

    # Find the target map element
    map_element = dash_duo.driver.find_element(By.ID, "england_map")

    # Use ActionChains to move to the center of the map element
    ActionChains(dash_duo.driver).move_to_element(map_element).perform()
    ActionChains(dash_duo.driver).move_by_offset(0, 0.).perform()
    ActionChains(dash_duo.driver).move_by_offset(0, 0).perform()
    ActionChains(dash_duo.driver).move_by_offset(0, 0).perform()
    ActionChains(dash_duo.driver).move_by_offset(0, 0).perform()
    
    # Wait for the card to appear
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "card-body"))
    )

    # Get the updated number of cards
    updated_num_cards = len(dash_duo.driver.find_elements(By.CLASS_NAME, "card-body"))

    # Get the text of the h6 element in the card
    card_text = dash_duo.driver.find_element(By.ID, "card").find_element(By.TAG_NAME, "h6").text

    # Assert that the number of cards has increased by 1
    assert updated_num_cards == (initial_num_cards + 1)

    # Assert that the card text is not empty
    assert card_text != ""

def test_dropdown_map_updates(dash_duo):
    """
    GIVEN the app is running which has a <div id='map'>
    WHEN a region is selected from the region dropdown
    THEN the HEI dropdown should update accordingly
    AND the number of groups in the legend should be 1
    """
    
    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Wait for the map to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#england_map > div.js-plotly-plot > div > div > svg:nth-child(5)"))
    )
    
    time.sleep(5)

    #Find hei dropdown element
    hei_dropdown_element = dash_duo.driver.find_element(By.ID, "hei-dropdown-map")
    hei_dropdown_element.click()

    #Count the number of option elements in the dropdown menu
    initial_hei_menu = dash_duo.driver.find_elements(By.CLASS_NAME, "VirtualizedSelectOption")
    initial_num_options = len(initial_hei_menu)

    #Find the region dropdown element
    region_dropdown_element = dash_duo.driver.find_element(By.ID, "region-dropdown-map")
    region_dropdown_element.click()

    #Find the region dropdown menu
    region_dropdown_menu = dash_duo.driver.find_element(By.CLASS_NAME, "Select-menu-outer")

    #Click the first option in the region dropdown
    ActionChains(dash_duo.driver).click(region_dropdown_menu).perform()

    #Wait for the region dropdown to disappear
    WebDriverWait(dash_duo.driver, 30).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "Select-menu-outer"))
    )

    time.sleep(3)

    #Find hei dropdown element
    element = dash_duo.driver.find_element(By.ID,"hei-dropdown-map")
    dash_duo.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()

    #Count the number of option elements in the dropdown menu
    updated_hei_menu = dash_duo.driver.find_elements(By.CLASS_NAME, "VirtualizedSelectOption")
    updated_num_options = len(updated_hei_menu)

    #Get the updates number of groups in the legend
    updated_group = dash_duo.driver.find_elements(By.CLASS_NAME, "legendtext")
    updated_num_groups = len(updated_group)

    #Assert that the number of options in the hei dropdown has changed
    assert updated_num_options < initial_num_options

    #Asser the number of groups in the legend is now 1
    assert updated_num_groups == 1

def test_map_card_link_opens(dash_duo):
    """
    GIVEN the app is running which has a <div id='map>
    WHEN a marker in the map is selected
    THEN there should be a card on the page
    AND the card should contain a link
    WHEN the link is clicked
    THEN the page should navigate to the university overview page
    """
    
    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Wait for the map to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#england_map > div.js-plotly-plot > div > div > svg:nth-child(5)"))
    )

    # Find the target map element
    map_element = dash_duo.driver.find_element(By.ID, "england_map")

    # Use ActionChains to move to the center of the map element
    ActionChains(dash_duo.driver).move_to_element(map_element).perform()
    ActionChains(dash_duo.driver).move_by_offset(0, 0.).perform()
    ActionChains(dash_duo.driver).move_by_offset(0, 0).perform()
    ActionChains(dash_duo.driver).move_by_offset(0, 0).perform()
    ActionChains(dash_duo.driver).move_by_offset(0, 0).perform()

    # Wait for the card to appear
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "card"))
    )

    # Get the card element
    card = dash_duo.driver.find_element(By.CLASS_NAME, "card")

    # Get the header in the card which is a link
    link = card.find_element(By.TAG_NAME, "H4")

    # Click on the link
    link.click()

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.url_contains('/university/')
    )

    # Assert that the URL has changed to the university overview page
    assert '/university/' in dash_duo.driver.current_url

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
    year_dropdown = dash_duo.driver.find_element(By.ID, "year-dropdown-comparison")
    class_dropdown = dash_duo.driver.find_element(By.ID, "class-dropdown-comparison")
    category_marker_dropdown = dash_duo.driver.find_element(By.ID, "category-marker-dropdown-comparison")
    category_dropdown = dash_duo.driver.find_element(By.ID, "category-dropdown-comparison")
    hei_dropdown = dash_duo.driver.find_element(By.ID, "hei-dropdown-comparison")

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

    #Get the category marker dropdown element
    category_marker_dropdown_element = dash_duo.driver.find_element(By.ID, "category-marker-dropdown-comparison")

    # Initialize Select object for the category marker dropdown
    category_marker_dropdown = Select(category_marker_dropdown_element)

    # Select the option with value "Grounds area"
    category_marker_dropdown.select_by_value("Grounds area")

    #Get the category dropdown element
    category_dropdown_element = dash_duo.driver.find_element(By.ID, "category-dropdown-comparison")

    # Initialize Select object for the category dropdown
    category_dropdown = Select(category_dropdown_element)

    # Select the option with value "Water (hectares)"
    category_dropdown.select_by_value("Water (hectares)")

    #Click the HEI dropdown element
    hei_dropdown_element = dash_duo.driver.find_element(By.ID, "hei-dropdown-comparison")
    hei_dropdown_element.click()

    #Find the hei dropdown menu
    hei_dropdown_menu = dash_duo.driver.find_element(By.CLASS_NAME, "Select-menu-outer")
    #Click the first option in the dropdown
    ActionChains(dash_duo.driver).click(hei_dropdown_menu).perform()

    time.sleep(3)

    # Get the initial bar chart content
    initial_bar_chart_content = dash_duo.find_element("#bar_chart").text

    #Enter another option in the HEI dropdown
    hei_dropdown_element.click()
    hei_dropdown_menu = dash_duo.driver.find_element(By.CLASS_NAME, "Select-menu-outer")
    ActionChains(dash_duo.driver).click(hei_dropdown_menu).perform()

    time.sleep(2)

    # Get the updated bar chart content
    updated_bar_chart_content = dash_duo.find_element("#bar_chart").text

    # Assert that the bar chart content has been updated
    assert updated_bar_chart_content != initial_bar_chart_content

def test_overview_page_layout(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user navigates to the overview page
    THEN the layout should contain the expected components
    """

    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the overview page
    dash_duo.driver.get(dash_duo.server_url + '/university/University College London')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 60).until(
        EC.presence_of_element_located((By.ID, "overview_line_chart"))
    )

    # Get the layout elements
    class_dropdown = dash_duo.driver.find_element(By.ID, "class-dropdown")
    category_marker_dropdown = dash_duo.driver.find_element(By.ID, "category-marker-dropdown")
    toggle_button = dash_duo.driver.find_element(By.ID, "toggle")

    # Assert that the layout contains the expected components
    assert class_dropdown.is_displayed()
    assert category_marker_dropdown.is_displayed()
    assert toggle_button.is_displayed()

def test_overview_update_line_chart(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user goes to the overview page of University College London
    AND selects a category marker from the dropdown
    THEN the line chart should update accordingly
    """
    
    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the overview page
    dash_duo.driver.get(dash_duo.server_url + '/university/University College London')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.ID, "overview_line_chart"))
    )

    # Get the initial line chart content
    initial_line_chart_content = dash_duo.find_element("#overview_line_chart").text

    #Get the category marker dropdown element
    category_marker_dropdown_element = dash_duo.driver.find_element(By.ID, "category-marker-dropdown")

    # Initialize Select object for the category marker dropdown
    category_marker_dropdown = Select(category_marker_dropdown_element)

    # Select the option with value "Grounds area"
    category_marker_dropdown.select_by_value("Grounds area")

    # Wait for the line chart content to change
    WebDriverWait(dash_duo.driver, 30).until(
        lambda driver: dash_duo.find_element("#overview_line_chart").text != initial_line_chart_content
    )

    # Get the updated line chart content
    updated_line_chart_content = dash_duo.find_element("#overview_line_chart").text

    # Assert that the line chart content has been updated
    assert updated_line_chart_content != initial_line_chart_content

def test_toggle_sidebar_button(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user goes to the overview page of University College London
    AND clicks on the toggle sidebar button
    THEN the sidebar should expand accordingly
    """
    
    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the overview page
    dash_duo.driver.get(dash_duo.server_url + '/university/University College London')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.ID, "collapse"))
    )

    # Get the toggle button
    toggle_button = dash_duo.find_element("#toggle")

    # Click on the toggle button
    toggle_button.click()

    # Wait for the sidebar to expand
    WebDriverWait(dash_duo.driver, 30).until(
        EC.visibility_of_element_located((By.ID, "collapse"))
    )

    # Get the updated state of the sidebar
    updated_sidebar_state = dash_duo.find_element("#collapse").get_attribute("class")

    # Assert that the sidebar has expanded
    assert "show" in updated_sidebar_state

    # Click on the toggle button again
    toggle_button.click()

    # Wait for the sidebar to collapse
    WebDriverWait(dash_duo.driver, 30).until(
        EC.invisibility_of_element_located((By.ID, "collapse"))

    )

    # Get the updated state of the sidebar
    updated_sidebar_state = dash_duo.find_element("#collapse").get_attribute("class")

    # Assert that the sidebar has collapsed
    assert "show" not in updated_sidebar_state
    
def test_sidebar_search(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user goes to the overview page of University College London
    AND clicks on the toggle sidebar button
    AND enters a search term in the sidebar search input
    THEN the sidebar should display only the universities that match the search term
    """
    
    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the overview page
    dash_duo.driver.get(dash_duo.server_url + '/university/University College London')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.ID, "collapse"))
    )

    # Click on the toggle button
    toggle_button = dash_duo.find_element("#toggle")
    toggle_button.click()

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

    #Check that the universities displayed in the sidebar are the ones that match the search term
    nav_links = dash_duo.find_elements(".sidebar-nav-link")
    for nav_link in nav_links:
        assert "Bath" in nav_link.text, f"Expected 'Bath' in nav link text, but got: {nav_link.text}"

def test_sidebar_link(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user goes to the overview page of University College London
    AND clicks on a university link in the sidebar
    THEN the page should navigate to the overview page of the selected university
    """
    
    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the overview page
    dash_duo.driver.get(dash_duo.server_url + '/university/University College London')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.ID, "collapse"))
    )

    # Click on the toggle button
    toggle_button = dash_duo.find_element("#toggle")
    toggle_button.click()

    WebDriverWait(dash_duo.driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#sidebar-nav > a:nth-child(1)"))
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

def test_non_existent_university_overview(dash_duo):
    """
    GIVEN the Dash app is running
    WHEN the user goes to the overview page of a non-existent university
    THEN the app should display a message that the university was not found
    """
    
    # Get the Dash app
    app = import_app(app_file='app')

    # Start the Dash app
    dash_duo.start_server(app)

    # Navigate to the overview page of a non-existent university
    dash_duo.driver.get(dash_duo.server_url + '/university/Non Existent University')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )

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
    dash_duo.driver.get(dash_duo.server_url + '/university/University College London')

    # Wait for the page to load
    WebDriverWait(dash_duo.driver, 30).until(
        EC.presence_of_element_located((By.ID, "category-marker-dropdown"))
    )

    # Initialise the Select object for the category marker dropdown
    category_marker_dropdown_element = dash_duo.driver.find_element(By.ID, "category-marker-dropdown")
    category_marker_dropdown = Select(category_marker_dropdown_element)

    # Get the initial state of the category marker dropdown options and value
    initial_options = [option.text for option in category_marker_dropdown.options]
    initial_value = category_marker_dropdown.first_selected_option.text

    # Simulate not selecting any option from the class dropdown to trigger the callback
    class_dropdown_element = dash_duo.driver.find_element(By.ID, "class-dropdown")
    class_dropdown = Select(class_dropdown_element)
    class_dropdown.select_by_value("")

    # Get the updated state of the category marker dropdown options and value
    updated_options = [option.text for option in category_marker_dropdown.options]
    updated_value = category_marker_dropdown.first_selected_option.text

    # Assert that options and value remain unchanged
    assert initial_options == updated_options
    assert initial_value == updated_value







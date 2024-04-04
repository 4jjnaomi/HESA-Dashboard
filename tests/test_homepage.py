import time
from dash.testing.application_runners import import_app

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

def test_region_dropdown_map_updates(dash_duo):
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
    region_dropdown_menu.click()
    #ActionChains(dash_duo.driver).click(region_dropdown_menu).perform()
    #Select the region dropdown input
    region_dropdown_input = dash_duo.driver.find_element(By.CSS_SELECTOR, "#react-select-6--value > div.Select-input > input")
    region_dropdown_input.send_keys("North East")
    region_dropdown_input.send_keys(Keys.RETURN)

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
    ActionChains(dash_duo.driver).move_by_offset(0, 0.001).perform()
    ActionChains(dash_duo.driver).move_by_offset(0, 0).perform()
    ActionChains(dash_duo.driver).move_by_offset(0, 0.001).perform()
    ActionChains(dash_duo.driver).move_by_offset(0.001, 0).perform()


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

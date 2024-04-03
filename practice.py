from selenium import webdriver
from selenium.webdriver.common.by import By
import time

time.sleep(5)

# Start a Selenium WebDriver session
driver = webdriver.Chrome()

# Navigate to your Dash app
driver.get("http://127.0.0.1:8051/")

time.sleep(10)

# Identify the england_map element
england_map_element = driver.find_element(By.ID, "england_map")

# Construct the JavaScript code to simulate hover on a specific point
javascript_code = """
// Simulate hover action on the map at a specific point
var hoverData = {
  points: [{
    customdata: "10007149"  // Specify the custom data for the point
  }]
};

// Find the target map element
var mapElement = document.getElementById("england_map");

// Create a MouseEvent for mouseover event
var event = new MouseEvent('mouseover', {
  bubbles: true,
  cancelable: true,
});

// Dispatch the mouseover event to the target element
mapElement.dispatchEvent(event);
"""

# Execute the JavaScript code
driver.execute_script(javascript_code)

time.sleep(5)

# Close the Selenium WebDriver session
driver.quit()


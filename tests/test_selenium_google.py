from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def test_google_search():
    driver = webdriver.Chrome()  # Use Chrome WebDriver
    driver.get("https://www.google.com")  # Open Google

    # Assert the title contains "Google"
    assert "Google" in driver.title, "Google is not in the page title."

    # Find the search box, enter a query, and press Enter
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Jenkins CI/CD" + Keys.RETURN)
    time.sleep(2)  # Wait for results to load

    # Check if search results appear
    results = driver.find_elements(By.CSS_SELECTOR, "div.g")
    assert len(results) > 0, "No search results found."

    print("Test passed: Google Search works.")
    driver.quit()


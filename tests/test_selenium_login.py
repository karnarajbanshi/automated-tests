from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_login_page():
    driver = webdriver.Chrome()  # Use Chrome WebDriver
    driver.get("http://example.com/login")  # Replace with your login page URL

    # Assert the title contains "Login"
    assert "Login" in driver.title, "Login is not in the page title."

    # Find and interact with username and password fields
    username_field = driver.find_element(By.ID, "username")  # Replace 'username' with actual ID
    password_field = driver.find_element(By.ID, "password")  # Replace 'password' with actual ID
    login_button = driver.find_element(By.ID, "login-button")  # Replace 'login-button' with actual ID

    username_field.send_keys("testuser")
    password_field.send_keys("password123")
    login_button.click()
    time.sleep(2)  # Wait for the page to load

    # Check for login success by finding a unique element
    success_message = driver.find_element(By.ID, "welcome-message")  # Replace with actual element
    assert success_message.is_displayed(), "Login test failed."

    print("Test passed: Login works.")
    driver.quit()


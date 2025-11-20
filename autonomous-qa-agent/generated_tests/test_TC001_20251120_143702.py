from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_valid_login():
    try:
        # Initialize Chrome driver with webdriver-manager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        
        # Step 1: Launch IMDb website
        driver.get("https://www.imdb.com/")
        print("IMDb homepage loaded")
        
        # Step 2: Click Sign In button
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign In"))
        )
        sign_in_button.click()
        print("Clicked Sign In button")
        
        # Step 3: Enter valid email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        email_field.send_keys("valid_email@example.com")
        print("Entered valid email")
        
        # Step 4: Enter valid password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        password_field.send_keys("ValidPassword123!")
        print("Entered valid password")
        
        # Step 5: Click Sign In button
        sign_in_submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signInSubmit"))
        )
        sign_in_submit.click()
        print("Clicked Sign In button")
        
        # Verify successful login - check for account page element
        WebDriverWait(driver, 15).until(
            EC.url_contains("/profile")
        )
        print("Login successful - redirected to account page")
        
        # Keep browser open for 5 seconds to verify result
        time.sleep(5)
        
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    test_valid_login()
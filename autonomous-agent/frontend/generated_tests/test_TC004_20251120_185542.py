from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def test_discount_code_with_spaces():
    try:
        # Initialize Chrome driver with WebDriver Manager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        # Open test website (replace with actual URL)
        driver.get("https://example-checkout.com")
        
        # Wait object with 10s timeout
        wait = WebDriverWait(driver, 10)
        
        # Step 1: Enter ' SAVE15 ' in discount code field
        discount_code_field = wait.until(EC.presence_of_element_located((By.ID, "discount-code")))
        discount_code_field.clear()
        discount_code_field.send_keys(" SAVE15 ")  # Includes leading/trailing spaces
        
        # Step 2: Click apply discount button
        apply_button = wait.until(EC.element_to_be_clickable((By.ID, "apply-discount")))
        apply_button.click()
        
        # Step 3: Verify discount rate is 0.15 (15%)
        discount_rate_element = wait.until(EC.presence_of_element_located((By.ID, "discount-rate")))
        discount_rate_text = discount_rate_element.text
        
        # Convert percentage text to decimal for validation
        assert discount_rate_text == "15%", f"Expected discount rate 15%, got {discount_rate_text}"
        
        # Step 4: Verify success message is displayed
        success_message = wait.until(EC.presence_of_element_located((By.ID, "discount-message")))
        assert success_message.text == "15% Discount Applied!", f"Unexpected message: {success_message.text}"
        
        print("Test TC004 Passed: Discount applied correctly with spaces")
        
    except TimeoutException as te:
        print(f"Test TC004 Failed: Element not found within timeout - {str(te)}")
    except NoSuchElementException as ne:
        print(f"Test TC004 Failed: Element not found - {str(ne)}")
    except AssertionError as ae:
        print(f"Test TC004 Failed: Validation error - {str(ae)}")
    except Exception as e:
        print(f"Test TC004 Failed with unexpected error: {str(e)}")
    finally:
        # Close browser after test
        time.sleep(2)  # Brief delay to view results
        driver.quit()

# Run the test
test_discount_code_with_spaces()
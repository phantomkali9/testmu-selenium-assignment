import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("driver")
class TestSeleniumAssignment:

    def test_scenario_1_simple_form(self, driver):
        """
        Test Scenario 1: Simple Form Demo validation
        1. Open TestMu AI Selenium Playground[cite: 22]
        2. Click 'Simple Form Demo'[cite: 22]
        3. Validate URL contains 'simple-form-demo'[cite: 22]
        4. Enter message via variable[cite: 22, 23]
        5. Click 'Get Checked Value' & validate right-hand panel[cite: 23]
        """
        wait = WebDriverWait(driver, 20)
        
        # 1. Open Playground
        driver.get("https://www.testmuai.com/selenium-playground/")
        
        # 2. Click "Simple Form Demo" (Using Link Text locator)
        simple_form_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Simple Form Demo"))
        )
        simple_form_link.click()
        
        # 3. Validate URL
        assert "simple-form-demo" in driver.current_url, f"Expected URL to contain 'simple-form-demo', got {driver.current_url}"
        
        # 4 & 5. Create variable and enter value in 'Enter Message' box (Using ID locator)
        message_text = "Welcome to TestMu AI"
        message_input = wait.until(
            EC.visibility_of_element_located((By.ID, "user-message"))
        )
        message_input.clear()
        message_input.send_keys(message_text)
        
        # 6. Click 'Get Checked Value' button (Using XPath locator)
        get_value_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Get Checked Value']"))
        )
        get_value_btn.click()
        
        # 7. Validate text message displayed in the right-hand panel (Using CSS Selector locator)
        output_message = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "p#message"))
        )
        assert output_message.text == message_text, f"Expected message '{message_text}', got '{output_message.text}'"

    def test_scenario_2_drag_and_drop_slider(self, driver):
        """
        Test Scenario 2: Drag & Drop Sliders validation
        1. Open page and click 'Drag & Drop Sliders'[cite: 23]
        2. Select slider 'Default value 15' and drag to 95[cite: 23]
        """
        wait = WebDriverWait(driver, 20)
        
        # 1. Open Playground & click feature
        driver.get("https://www.testmuai.com/selenium-playground/")
        
        slider_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Drag & Drop Sliders"))
        )
        slider_link.click()
        
        # 2. Locate slider with default value 15 (Using XPath)
        # Typically the range input associated with default value 15
        slider = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h4[contains(text(),'Default value 15')]/following-sibling::div//input[@type='range']"))
        )
        output_range = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h4[contains(text(),'Default value 15')]/following-sibling::div//output[@id='range']"))
        )

        # Use ActionChains or script execution to adjust slider range precisely to 95
        # Moving slider via offset or setting value property directly via JavaScript if native drag is constrained
        driver.execute_script("arguments[0].value = '95'; arguments[0].dispatchEvent(new Event('input'));", slider)
        
        # Validate range value shows 95
        assert output_range.text == "95", f"Expected slider value to be '95', but got '{output_range.text}'"

    def test_scenario_3_input_form_submit(self, driver):
        """
        Test Scenario 3: Input Form Submit Validation
        1. Open page and click 'Input Form Submit'[cite: 23]
        2. Click Submit without filling info & assert validation error[cite: 23]
        3. Fill fields, select 'United States', and validate success message[cite: 23]
        """
        wait = WebDriverWait(driver, 20)
        
        # 1. Open Playground & click link
        driver.get("https://www.testmuai.com/selenium-playground/")
        
        form_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Input Form Submit"))
        )
        form_link.click()
        
        # 2. Click "Submit" button without filling information (Using XPath)
        submit_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']"))
        )
        submit_btn.click()
        
        # 3. Assert HTML5 validation message on Name field
        name_field = driver.find_element(By.ID, "name")
        validation_message = name_field.get_attribute("validationMessage")
        assert validation_message != "", "Expected validation error message on empty form submit."

        # 4. Fill in Name, Email, and other fields (Using IDs and Name locators)
        driver.find_element(By.ID, "name").send_keys("A Sri Vishnu")
        driver.find_element(By.ID, "inputEmail4").send_keys("vishnu.test@example.com")
        driver.find_element(By.ID, "inputPassword4").send_keys("SecurePassword123")
        driver.find_element(By.ID, "company").send_keys("GITAM University")
        driver.find_element(By.ID, "websitename").send_keys("https://github.com")
        
        # 5. Select "United States" from Country dropdown using text property (Using Tag/XPath combination)
        country_dropdown = wait.until(
            EC.element_to_be_clickable((By.NAME, "country"))
        )
        for option in country_dropdown.find_elements(By.TAG_NAME, "option"):
            if option.text.strip() == "United States":
                option.click()
                break

        driver.find_element(By.ID, "inputCity").send_keys("Visakhapatnam")
        driver.find_element(By.ID, "inputAddress1").send_keys("Beach Road")
        driver.find_element(By.ID, "inputAddress2").send_keys("Near RK Beach")
        driver.find_element(By.ID, "inputState").send_keys("Andhra Pradesh")
        driver.find_element(By.ID, "inputZip").send_keys("530003")

        # 6. Click Submit again with all fields filled
        submit_btn.click()

        # 7. Validate success message
        success_msg_elem = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//p[@class='success-msg']"))
        )
        expected_success = "Thanks for contacting us, we will get back to you shortly."
        assert expected_success in success_msg_elem.text, f"Expected success message '{expected_success}', got '{success_msg_elem.text}'"
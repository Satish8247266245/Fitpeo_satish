from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up the WebDriver (assuming ChromeDriver is in the PATH)
driver = webdriver.Chrome()



try:
    # Navigate to the FitPeo Homepage
    driver.get("https://www.fitpeo.com")
    driver.maximize_window()

    # Wait for the page to load and navigate to the Revenue Calculator page
    wait = WebDriverWait(driver, 10)
    revenue_calculator_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Revenue Calculator")))
    revenue_calculator_link.click()

    # Scroll down to the slider section
    slider_section = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='MuiSlider-rail css-3ndvyc']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", slider_section)

    # Adjust the slider to set its value to 820
    slider = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='MuiSlider-rail css-3ndvyc']")))
    action = ActionChains(driver)
    # action.click_and_hold(slider).move_by_offset(820, 0).release().perform()
    action.click_and_hold(slider).move_by_offset(820, 0).release().perform()

    # Verify the slider value is set to 820
    slider_value = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id=':r0:']")))
    # driver.find_element(By.XPATH, "//input[@id=':r0:']").send_keys("820")
    # assert slider_value == "820"
    assert slider_value.get_attribute("value") == "820"

    # Update the text field to 560
    text_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id=':r0:']")))
    text_field.clear()
    text_field.send_keys("560")

    # Validate slider value is updated to 560
    slider_value = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id=':r0:']")))
    assert slider_value.get_attribute("value") == "560"

    # Select CPT Codes
    cpt_codes = ["CPT-99091", "CPT-99453", "CPT-99454", "CPT-99474"]
    for code in cpt_codes:
        checkbox = wait.until(EC.element_to_be_clickable((By.ID, code)))
        if not checkbox.is_selected():
            checkbox.click()

    # Validate Total Recurring Reimbursement
    reimbursement_header = wait.until(EC.presence_of_element_located((By.ID, "total-reimbursement")))
    assert "Total Recurring Reimbursement for all Patients Per Month: $110700" in reimbursement_header.text

finally:
    # Close the browser
    driver.quit()

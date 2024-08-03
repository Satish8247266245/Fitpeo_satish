from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up the WebDriver (assuming ChromeDriver is in the PATH)
driver = webdriver.Chrome()
'''serv_obj = Service("C:\\chromedriver.exe")
driver = webdriver.Chrome(service=serv_obj)'''


try:
    # Navigate to the FitPeo Homepage
    driver.get("https://www.fitpeo.com")
    driver.maximize_window()

    # Wait for the page to load and navigate to the Revenue Calculator page
    wait = WebDriverWait(driver, 10)
    revenue_calculator_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Revenue Calculator")))
    revenue_calculator_link.click()

    # Step 3: Scroll down to the Slider section
    slider = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='MuiSlider-rail css-3ndvyc']")))
    driver.execute_script("arguments[0].scrollIntoView();", slider)
    time.sleep(1)

    # Step 4: Adjust the Slider to 820
    slider_handle = driver.find_element(By.XPATH, "//input[@type='range']")
    driver.execute_script("arguments[0].value = arguments[1];", slider_handle, 820)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", slider_handle)
    time.sleep(1)

    # Validate the slider value is updated to 820
    updated_slider_value = slider_handle.get_attribute('value')
    assert updated_slider_value == '820', f"Slider value is not updated to 820, but to {updated_slider_value}"


    # Step 5: Update the Text Field to 560
    text_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id=':r0:']")))
    text_field.clear()
    text_field.send_keys("560")

    # Step 6: Select the CPT codes
    cpt_codes = ['CPT-99091', 'CPT-99453', 'CPT-99454', 'CPT-99474']
    for code in cpt_codes:
        checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
        if not checkbox.is_selected():
            checkbox.click()

    # Step 7: Validate the total recurring reimbursement value
    total_reimbursement = driver.find_element(By.XPATH, "//p[contains(@class, 'MuiTypography-body1')]" )  # Replace with actual ID
    assert total_reimbursement.text == '$110700', "Total Recurring Reimbursement is not $110700"


finally:
    # Close the browser
    driver.quit()



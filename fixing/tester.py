import datetime
import time
import numpy as np
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# from email_sender import send_email

url = 'https://visas-de.tlscontact.com/visa/tn/tnTUN2de/home'

options = uc.ChromeOptions()

options.add_argument("--start-maximized")

driver = uc.Chrome(options=options,
                   use_subprocess=True)

driver.get(url)
time.sleep(5)
input("Press Enter to continue...")
def wait_for_display_none(driver, locator):
    element = driver.find_element(*locator)
    return element.value_of_css_property('display') == 'none'


# Define the locator for the div element
locator = (By.XPATH, '//div[contains(@class, "vld-overlay")]')

time.sleep(abs(np.random.normal(20, 2)))

WebDriverWait(driver, 120).until(EC.presence_of_element_located(
    (By.CLASS_NAME, "tls-button-link")))

driver.find_elements(By.CLASS_NAME, "tls-button-link")[0].click()

WebDriverWait(driver, 120).until(EC.presence_of_element_located(
    (By.NAME, "username")))
time.sleep(abs(np.random.normal(10, 2)))

driver.find_element(By.NAME, "username").send_keys("typec25@gmx.fr")

time.sleep(abs(np.random.normal(5, 2)))

driver.find_element(By.NAME, "password").send_keys("Azerty123**")

time.sleep(abs(np.random.normal(5, 2)))

actions = ActionChains(driver)
actions.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

time.sleep(abs(np.random.normal(10, 2)))

WebDriverWait(driver, 120).until(EC.presence_of_element_located(
    (By.CLASS_NAME, "button-neo-inside")))
time.sleep(abs(np.random.normal(10, 2)))

driver.find_element(By.CLASS_NAME, "button-neo-inside").click()

time.sleep(abs(np.random.normal(20, 2)))

WebDriverWait(driver, 120).until(EC.presence_of_element_located(
    (By.CLASS_NAME, "tls-button-primary.-bold")))

time.sleep(abs(np.random.normal(10, 2)))

driver.find_element(By.CLASS_NAME, "tls-button-primary.-bold").click()

no_rdv = "Désolé, il n'y a pas de rendez-vous disponible pour le moment, veuillez vérifier plus tard."

time.sleep(abs(np.random.normal(20, 2)))

pageSource = driver.page_source

while True:
    # Wait for the div to have 'display: none'
    WebDriverWait(driver, 60).until(lambda driver: wait_for_display_none(driver, locator))
    time.sleep(10)
    pageSource = driver.page_source

    if no_rdv in pageSource:
        print("no rdv")
        time.sleep(90)  # only 30 seconds

        driver.refresh()

        time.sleep(10)

    else:
        print("fama rdv")
        # send_email("")
        time.sleep(90)  # only 30 seconds

        driver.refresh()

        time.sleep(10)



from webdriver_manager.chrome import ChromeDriverManager

# Download and install the latest ChromeDriver
driver_path = ChromeDriverManager(version="92.0.4515.107").install()
print(driver_path)
# Use the driver_path in your Selenium script
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
br = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
br.get("https://www.google.com/")

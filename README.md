# easy
It's an easy interface to Selenium commands. Help the project to grow!


# Simple example

```
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from automation import automation


DRIVER_DIR=./chromedriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=DRIVER_DIR, options=chrome_options)
automation = BaseObjects(driver)
automation.navigate_to("www.google.com")
automation.get_all_elements("xpath", "input")  # get all inputs
```

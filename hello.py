server = 'http://localhost:4723/wd/hub'
desired_caps = {
    "platformName": "Android",
    "deviceName": "SM_G9860",
    "appPackage": "com.tencent.mm",
    "appActivity": ".ui.LauncherUI"
}

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Remote(server,desired_caps)

wait = WebDriverWait(driver,30)
login = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/fam')))
login.click()
phone = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/bhn')))
phone.send_keys("13047211898")
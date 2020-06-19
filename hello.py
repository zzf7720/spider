from chaojiying import Chaojiying_Client
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from io import BytesIO
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

PHONE_NUMBER = '13047211898'
PASSWORD = 'bluesky'
CHAOJIYING_USERNAME = '772091199'
CHAOJIYING_PASSWORD = 'bluesky'
CHAOJIYING_SOFT_ID = 905945
CHAOJIYING_KIND = 9004

class Crack_Bilibli():
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,20)
        self.number = PHONE_NUMBER
        self.password = PASSWORD
        self.chaojiying = Chaojiying_Client(CHAOJIYING_USERNAME,CHAOJIYING_PASSWORD,CHAOJIYING_SOFT_ID)

    def open(self):
        self.browser.get(self.url)
        user_name = self.wait.until(EC.presence_of_element_located((By.ID,'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID,'login-passwd')))
        user_name.send_keys(self.number)
        password.send_keys(self.password)

    def get_button(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'btn-login')))
        return button

    def get_click_element(self):
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_medium_fontsize')))
        return element

    def get_position(self):
        element = self.get_click_element()
        time.sleep(2)
        location = element.location
        size = element.size
        top,bottom,left,right = location['y'],location['y'] + size['height'],location['x'],location['x'] + size['width']
        suofang = 125/100
        return (top*suofang,bottom*suofang,left*suofang,right*suofang)
        # return (top,bottom,left,right)

    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()

        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_image(self,name='captcha.png'):
        top,bottom,left,right = self.get_position()
        print('验证码位置',top,bottom,left,right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left,top,right,bottom))
        # captcha.show()
        captcha.save(name)
        return captcha

    def get_point(self,captcha_result):
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self,locations):
        for location in locations:
            location_1 = location[0] - 25
            location_2 = location[1] -30
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_click_element(),location_1,location_2).click().perform()
            time.sleep(1)

    def touch_click_verify(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_commit_tip')))
        button.click()

    def crack(self):
        self.open()
        button = self.get_button()
        button.click()
        image = self.get_image()
        bytes_item = BytesIO()
        image.save(bytes_item, format='PNG')
        result = self.chaojiying.PostPic(bytes_item.getvalue(),CHAOJIYING_KIND)
        print(result)
        locations = self.get_point(result)
        self.touch_click_words(locations)
        self.touch_click_verify()
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'bilifont bili-icon_fenqudaohang_shouye')))
            print('登入成功')
        except TimeoutException:
            self.crack()



if __name__ == '__main__':
    crack = Crack_Bilibli()
    crack.crack()












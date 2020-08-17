import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver_path = r'D:\eng\chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)
driver.get('http://www.hsydata.com/home/user')

element1 = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'anticon'))
)

switch = driver.find_element_by_xpath("//div[contains(@class,'ant-tabs-tab')][2]//i[@class='anticon']")
switch.click()
time.sleep(0.5)
username = driver.find_element_by_xpath("//form[contains(@class,'ant-form ant-form-horizontal')]/div[1]//input")
username.send_keys("18653195606")
password = driver.find_element_by_xpath("//form[contains(@class,'ant-form ant-form-horizontal')]/div[2]//input")
password.send_keys("skd158")

login_button = driver.find_element_by_xpath("//span[@class='ant-form-item-children']/button")
login_button.click()

elemen2 = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'ant-table-tbody'))
)
time.sleep(0.5)

for i in range(5):
    ps = driver.find_elements_by_xpath("//tbody[@class='ant-table-tbody']/tr//p")
    for p in ps:
        with open('top_100_up_list.txt', 'a+', encoding='utf-8') as fp:
            fp.write(p.text+'\n')
        print(p.text)
    time.sleep(3)




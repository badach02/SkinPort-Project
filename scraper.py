import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_url = "https://skinport.com/signin"
chrome_options = webdriver.ChromeOptions()# set a headless driver
user_agent = 'Mozilla/5.0 (X11; Linux x86_647) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options = chrome_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=chrome_options)
driver.get(start_url)

wait = WebDriverWait(driver, 10)

time.sleep(5)

username_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='email']")))
password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='password']")))
login_button = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div/form/div[2]/button")))
cookies_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div[4]/div/div[2]/button[2]")))

username = ""
password = ""

cookies_button.click()

time.sleep(2)

for character in username:
    wait_num = random.randint(100, 150)
    wait_num = wait_num / 1000
    time.sleep(wait_num)
    username_field.send_keys(character)

time.sleep(2)

for character in password:
    wait_num = random.randint(100, 150)
    wait_num = wait_num / 1000
    time.sleep(wait_num)
    password_field.send_keys(character)

time.sleep(2)

login_button.click()

time.sleep(100)

driver.quit()

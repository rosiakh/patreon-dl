import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome('C:\\Users\\Hubert\\Downloads\\chromedriver_win32\\chromedriver')
driver.get('https://www.patreon.com/login?ru=%2F')

email_element = driver.find_element_by_xpath('//*[@id="email"]')
email_element.send_keys('example@gmail.com')
email_text = email_element.text

pass_element = driver.find_element_by_xpath('//*[@id="password"]')
pass_element.send_keys('pass123')
pass_text = pass_element.text

login_button = driver.find_element_by_xpath(
    '//*[@id="renderPageContentWrapper"]/div/div/div/div/div[1]/div/form/button')
login_button.click()

driver.get('https://www.patreon.com/posts/16489306')  # breakpoint here to solve captcha

pattern = re.compile("^[0-9]+[.].*$")

links = driver.find_elements_by_xpath('//a[contains(@href, "https://www.patreon.com/posts")]')
lesson_hrefs = [link.get_attribute("href") for link in links if pattern.match(link.text)]
yt_hrefs = []

for lesson_href in lesson_hrefs:
    driver.get(lesson_href)

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="Start playback"]')))
    playback_button = driver.find_element_by_xpath('//*[@title="Start playback"]')
    playback_button.click()

    driver.switch_to.frame(driver.find_element_by_xpath('//iframe[starts-with(@src, "https://www.youtube.com/embed")]'))
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Play"]')))

    yt_button = driver.find_element_by_xpath('//a[@title="Watch on youtube.com"]')
    yt_href = yt_button.get_attribute('href')
    yt_hrefs.append(yt_href)

with open('hrefs.txt', 'w+') as f:
    for href in yt_hrefs:
        f.write(href + "\n")

driver.quit()

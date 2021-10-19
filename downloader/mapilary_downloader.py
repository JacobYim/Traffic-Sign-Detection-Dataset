from selenium import webdriver
import chromedriver_autoinstaller
import os
import time
import argparse

parser = argparse.ArgumentParser(description='This is macro for downloading Mapillary Traffic dataset')
parser.add_argument('id', type=str, help='id for Mapillary')
parser.add_argument('pw', type=str, help='password for Mapillary')
parser.add_argument('name', type=str, help='full name for terms of agreement')
parser.add_argument('headless', nargs='?', type=bool, default=False, help='whether run headless version or not')

args = parser.parse_args()

ID = args.id
PW = args.pw
NAME = args.name
chromedriver_autoinstaller.install()

chromeOptions = webdriver.ChromeOptions()
if args.headless :
    chromeOptions.add_argument("--headless") 
prefs = {"download.default_directory" : os.getcwd()+"/mapillary_data"}
chromeOptions.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(options=chromeOptions, )

driver.get('https://www.mapillary.com/dataset/trafficsign')
driver.find_element_by_xpath('/html/body/dataset-root/div/mtsd/div[1]/div/div[1]/dataset-download-request/button').click()

driver.find_element_by_xpath('//*[@id="login_form"]/form/div[2]/div[1]/input[1]').send_keys(ID)
driver.find_element_by_xpath('//*[@id="login_form"]/form/div[2]/div[1]/input[2]').send_keys(PW)
driver.find_element_by_xpath('//*[@id="login_form"]/form/div[2]/div[1]/div/button').click()

driver.implicitly_wait(1)

driver.find_element_by_xpath('/html/body/dataset-root/div/mtsd/div[1]/div/div[1]/dataset-download-request/button').click()
driver.implicitly_wait(1)
driver.find_element_by_xpath('/html/body/dataset-root/div/mtsd/div[1]/div/div[1]/dataset-download-request/app-fullscreen-modal/div[1]/section/form/div[1]/input').send_keys(NAME)
driver.find_element_by_xpath('/html/body/dataset-root/div/mtsd/div[1]/div/div[1]/dataset-download-request/app-fullscreen-modal/div[1]/section/form/div[2]/div[2]/input').click()
driver.implicitly_wait(1)
driver.find_element_by_xpath('/html/body/dataset-root/div/mtsd/div[1]/div/div[1]/dataset-download-request/app-fullscreen-modal/div[1]/section/form/div[3]/button').click()
time.sleep(2)
elems = driver.find_elements_by_class_name('text-decoration-none')
for elem in elems :
    if not 'mapillary' in elem.get_attribute("href") and not 'creativecommons' in elem.get_attribute("href") :
        elem.click()

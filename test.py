#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import shutil
import os
from termcolor import colored
import getpass

ID = input('[+] Enter username: ')
print(colored("Note: Password will not be echo...", 'cyan'))
PASSWORD = getpass.getpass(prompt='[+] Enter password: ')
url="https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip"
path=os.path.expanduser("~")+'/'
filename=url.split("/")[-1]
new_file=filename.split("_")[0]
PATH=path+new_file

def checking_system():

    print(colored("[+] Please wait, checking the system", 'cyan'))
    if os.path.exists(PATH):
        print(colored("[+] system is upto date", 'green'))
    else:
        print(colored("[-] driver is not found", 'red'))
        download_driver(url, path, filename, new_file)

def download_driver(url, path, filename, new_file):
    print(colored("[+] please wait, downloading the driver...", 'cyan'))
    r=requests.get(url, stream=True)
    with open(filename, "wb") as f:
        shutil.copyfileobj(r.raw, f)
    os.system(f"unzip {filename}")
    os.system(f"mv {new_file} {path}")
    os.system(f"rm {filename}")
    print(colored("[+] Successfully downloaded the driver...", 'green'))

checking_system()
# PATH = input('Enter driver path\n')
frequency = 3

def add(hour, val):
    return str(int(hour) + val)


def ryt_now():
    cur_time = time.localtime()
    cur_time = time.strftime("%H:%M:%S", cur_time)
    return cur_time


def get_time():
    cur_time = ryt_now()
    hour, mn, sec = cur_time.split(':')
    if int(mn) >= 40:
        hour = str((int(hour) + 1))
    return hour


def do_login(username, password):
    id_field = driver.find_element_by_xpath("//input[@placeholder='Username']")
    pass_field = driver.find_element_by_xpath("//input[@placeholder='Password']")

    id_field.send_keys(username)
    pass_field.send_keys(password)

    pass_field.send_keys(Keys.RETURN)
    message = driver.find_element_by_xpath("//a[@title='Click here to view Meetings']")
    message.send_keys(Keys.RETURN)


def process_hr(cur_hr, minutes):
    if int(cur_hr) > 12:
        cur_hr = str((int(cur_hr) - 12))
    cur = str((minutes + 60) % 60)
    if len(cur) < 2:
        cur = '0' + cur
    return cur_hr + ':' + cur


# check for classes from cur time t in order t - 1, t, t + 1
# handle false positive of night
def check_for_class(hour):
    print('Checking for ongoing class')
    for cur_hr in [add(hour, -2), add(hour, -1), hour, add(hour, 1)]:
        for minutes in range(0, 60):
            val = process_hr(cur_hr, minutes)
            # print('Checking class at', val)
            try:
                path = "//div[@data-start='" + val + "']"
                current_class = driver.find_element_by_xpath(path)
                print(val, ' - Class Found')
                current_class.find_element_by_xpath("./../..").send_keys(Keys.RETURN)
                return True
            except:
                pass
    return False


# not working
def greet():
    driver.switch_to.frame(driver.find_element_by_id('frame'))
    elem = driver.find_element_by_id('app')
    print(elem.get_attribute('role'))


# done
def do_polls(hour):
    print('Starting poll daemon')
    driver.switch_to.frame(driver.find_element_by_id('frame'))
    while get_time() <= hour:
        try:
            wait = WebDriverWait(driver, 3600)
            wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-labelledby="pollAnswerLabelA"]')))
            driver.find_element_by_xpath('//button[@aria-labelledby="pollAnswerLabelA"]').click()
        finally:
            pass
    return


def join():
    try:
        # wait = WebDriverWait(driver, 3600)
        # wait.until(EC.visibility_of_element_located(By.ID("//a[@role='button']")))niu
        driver.find_element_by_class_name('btn').send_keys(Keys.RETURN)
        time.sleep(6)
        driver.switch_to.frame(driver.find_element_by_id('frame'))
        driver.find_element_by_xpath('//button[@aria-label="Listen only"]').send_keys(Keys.RETURN)
        driver.switch_to.default_content()
        return True
    except:
        driver.quit()
        print('Join Button not available. Retrying in 3 minutes')
        time.sleep(3 * 60)
        return False


def abort():
    print('Aborting')
    driver.quit()
    exit(0)


for iterations in range(10):
    have_class = False
    for i in range(10):
        chrome_options = webdriver.ChromeOptions()
        # uncomment line below to hide the class tab
        # chrome_options.headless = True
        driver = webdriver.Chrome(PATH, options=chrome_options)
        driver.minimize_window()
        driver.get("http://myclass.lpu.in")

        try:
            do_login(ID, PASSWORD)
        except:
            print('Probably your credentials are invalid')
            abort()
        hr = get_time()
        if int(hr) >= 17:
            print(colored('No classes are scheduled after 5 pm', 'red'))
            abort()
        time.sleep(2)
        have_class = check_for_class(hr)
        if not have_class:
            print("No ongoing lectures found at", ryt_now())
            driver.quit()
            if i + 1 < 5:
                print('Sleeping for', frequency, 'minutes')
                time.sleep(frequency * 60)
            continue
        if join():
            have_class = True
            # greet()
            do_polls(hr)
            driver.quit()
            break
    if not have_class:
        time.sleep(15 * 60)

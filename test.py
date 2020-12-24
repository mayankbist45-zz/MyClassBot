from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from termcolor import colored
import stdiomask

ID = input('[+] Enter username:\n')
PASSWORD = stdiomask.getpass(prompt='[+] Enter password:\n')
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
# can be more efficient
def check_for_class(hour):
    print(colored('[+] Checking for ongoing class', 'cyan'))
    for cur_hr in [add(hour, -2), add(hour, -1), hour, add(hour, 1)]:
        for minutes in range(0, 60):
            val = process_hr(cur_hr, minutes)
            # print('Checking class at', val)
            try:
                path = "//div[@data-start='" + val + "']"
                current_class = driver.find_element_by_xpath(path)
                extra_check = current_class.get_attribute('data-full')
                if len(extra_check) > 8:
                    continue
                print(val, ' - Class Found')
                current_class.find_element_by_xpath("./../..").send_keys(Keys.RETURN)
                return val
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
    poll_number = 1
    cur_hour, cur_minutes = hour.split(':')
    cur_hour = int(cur_hour)
    cur_minutes = int(cur_minutes)
    cur_minutes += 5
    if cur_minutes > 59:
        cur_hour += 1
        cur_minutes %= 60
    cur_hour += 1
    print(colored('[+] Starting poll daemon', 'green'))
    print('End time estimated:', cur_hour, cur_minutes)
    driver.switch_to.frame(driver.find_element_by_id('frame'))

    print(ryt_now().split(':')[1], ryt_now().split(':')[0])
    while cur_minutes != int(ryt_now().split(':')[1]) and cur_hour <= int(ryt_now().split(':')[0]):
        try:
            wait = WebDriverWait(driver, 5)
            element = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[starts-with(@aria-labelledby,"pollAnswerLabel")]')))
            element.click()
            print('[+]', poll_number, 'poll(s) marked.')
            poll_number += 1
        except:
            pass


def join():
    try:
        # wait = WebDriverWait(driver, 3600)
        # wait.until(EC.visibility_of_element_located(By.ID("//a[@role='button']")))
        driver.find_element_by_class_name('btn').send_keys(Keys.RETURN)
        time.sleep(6)
        driver.switch_to.frame(driver.find_element_by_id('frame'))
        driver.find_element_by_xpath('//button[@aria-label="Listen only"]').send_keys(Keys.RETURN)
        driver.switch_to.default_content()
        return True
    except:
        driver.quit()
        print(colored('[-] Join Button not available. Retrying in 3 minutes', 'red', attrs=['reverse', 'blink']))
        time.sleep(3 * 60)
        return False


def abort():
    print(colored('[-] Aborting', 'red'))
    driver.quit()
    exit(0)


have_class = False
while True:
    chrome_options = webdriver.ChromeOptions()
    # uncomment line below to hide the class tab
    # chrome_options.headless = True
    # driver = webdriver.Chrome(PATH, options=chrome_options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # driver.minimize_window()
    driver.get("http://myclass.lpu.in")

    try:
        do_login(ID, PASSWORD)
    except:
        print(colored('[-] Probably your credentials are invalid', 'red'))
        abort()

    hr = get_time()
    if int(hr) >= 20:
        print(colored('[-] No classes are scheduled after 8 pm', 'cyan', attrs=['reverse', 'blink']))
        abort()

    have_class = check_for_class(hr)

    if have_class and join():
        do_polls(have_class)
        driver.quit()
        print(colored('[+] Class finished, Restarting Daemon For other classes', 'cyan'))
    else:
        print("No ongoing lectures found at", ryt_now())
        driver.quit()
        print('Sleeping for', frequency, 'minutes')
        time.sleep(frequency * 60)

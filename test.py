from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ID = input('Enter username:\n')
PASSWORD = input('Enter password:\n')
PATH = "/home/blackhawk/tools/webdriver/chrome/chromedriver"
# PATH = input('Enter driver path\n')
frequency = 3


def dec(hour):
    return str(int(hour) - 1)


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


# check for classes from cur time t in order t - 1, t, t + 1
# handle false positive of night
def check_for_class(hour):
    print('Checking for ongoing class')
    for minutes in range(-15, 31):
        cur_hr = hour
        if minutes < 0:
            cur_hr = dec(cur_hr)
        if int(cur_hr) > 12:
            cur_hr = str((int(cur_hr) - 12))
        cur = (minutes + 60) % 60
        cur = str(cur)
        if len(cur) < 2:
            cur = '0' + cur
        val = cur_hr + ':' + cur
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
    print('Frame switching successful')
    while get_time() <= hour:
        try:
            wait = WebDriverWait(driver, 3600)
            wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-labelledby="pollAnswerLabelA"]')))
            driver.find_element_by_xpath('//button[@aria-labelledby="pollAnswerLabelA"]').click()
        finally:
            pass
    # driver.find_element_by_xpath().click()
    return


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
        print('Join Button not available. Retrying in 3 minutes')
        time.sleep(3 * 60)
        return False


for iterations in range(10):
    have_class = False
    for i in range(10):
        driver = webdriver.Chrome(PATH)
        driver.get("http://myclass.lpu.in")
        do_login(ID, PASSWORD)
        hr = get_time()
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

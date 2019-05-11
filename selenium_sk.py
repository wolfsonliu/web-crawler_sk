import sys
import time
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from xml.etree import ElementTree

random.seed(1024)

def search_grant_by_year(driver, year):
    # select year
    lxtime = driver.find_element_by_name('lxtime')
    lxtime.send_keys(str(year))
    # search by year
    subdiv = driver.find_element_by_class_name('w980.clear.input00')
    submit = subdiv.find_elements_by_tag_name('input')[0]
    submit.click()


def get_page_data(driver):
    try:
        data_table = driver.find_element_by_class_name('jCarouselLite')
        data_data = data_table.find_element_by_xpath('//div/div/table/tbody')
        text = data_data.get_attribute('outerHTML')
        # problems start
        text = text.replace('" 一带一路"倡议在欧盟遭遇的挑战与对策研究"="', 'ydyl')
        # problems end
        table = ElementTree.fromstring(text)
        result = list()
        for x in table.findall('tr'):
            result.append('\t'.join([y[0].text if y[0].text else '' for y in x]))
        return result
    except NoSuchElementException:
        raise NoSuchElementException


def next_page(driver):
    page = driver.find_element_by_class_name('page.clear')
    next_page = page.find_element_by_link_text('下一页')
    next_page.click()
    time.sleep(random.uniform(0, 3))


def save_grant(driver, i, out_file):
    while True:
        try:
            tablerow = get_page_data(driver)
            with open(out_file, 'ab') as f:
                f.write(
                   ''.join(
                       [('\t'.join([str(i), y]) + '\n') for y in tablerow]
                   ).encode('utf-8')
                )
                i = i + 1
                # get new page
                next_page(driver)
        except NoSuchElementException:
            break
    return i


def save_grant_by_year(driver, year, i, out_file):
    search_grant_by_year(driver, year)
    newi = save_grant(driver, i, out_file)
    return newi
    return i


# process
if sys.platform == 'win32':
    ff = webdriver.Firefox(executable_path=r'./geckodriver.exe')
elif sys.platform == 'linux':
    ff = webdriver.Firefox(executable_path=r'./geckodriver')

ff.get('http://fz.people.com.cn/skygb/sk/index.php/Index/seach')

save_grant_by_year(ff, 2018, 1, 'sk_2018.csv')

save_grant(ff, 3, 'sk_2018.csv')

import os
import time
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from xml.etree import ElementTree

random.seed(1024)


def search_grant_info(driver, i, out_file):
    data_table = driver.find_element_by_class_name('jCarouselLite')
    data_head = data_table.find_element_by_xpath('//div/div/table/thead/tr')
#    with open(out_file, 'ab') as f:
#        the_head = ElementTree.fromstring(data_head.get_attribute('outerHTML'))
#        f.write(
#            (','.join(x.text.replace(' ', '') for x in the_head.getchildren()) + '/n').encode('utf-8')
#        )
    while True:
        try:
            data_table = driver.find_element_by_class_name('jCarouselLite')
            data_data = data_table.find_element_by_xpath('//div/div/table/tbody')
            table = ElementTree.fromstring(data_data.get_attribute('outerHTML'))
            with open(out_file, 'ab') as f:
                for x in table.findall('tr'):
                    f.write(
                        (
                            ','.join(
                                [str(i)] +
                                [y.getchildren()[0].text if y.getchildren()[0].text else '' for y in x.getchildren()]
                            ) + '\n'
                        ).encode('utf-8')
                    )
                    i = i + 1
            # get new page
            page = driver.find_element_by_class_name('page.clear')
            next_page = page.find_element_by_link_text('下一页')
            next_page.click()
            time.sleep(random.uniform(0, 3))
        except NoSuchElementException:
            break
    return i


ff = webdriver.Firefox(executable_path=r'./geckodriver.exe')
ff.get('http://fz.people.com.cn/skygb/sk/?&p=3094')
search_grant_info(ff, 61861, 'sk.csv')

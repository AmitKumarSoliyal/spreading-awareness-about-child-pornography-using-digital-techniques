from selenium import webdriver
import time
from secrets import username, password
import csv
browser = webdriver.Firefox()
#group_link = 'https://mbasic.facebook.com/groups/'#2540054519633368'
# Login
def login(username, password):
    browser.get('https://mbasic.facebook.com/')
    email_input = browser.find_element_by_id('m_login_email')
    password_input = browser.find_element_by_name('pass')
    # email_input = browser.find_element_by_id('email')
    # password_input = browser.find_element_by_name('pass')
    login_button = browser.find_element_by_name('login')
    email_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()
    ok_button = browser.find_element_by_xpath("//form/div/input")
    ok_button.click()

def write_message(link, message):
    browser.get(link)
    message_box = browser.find_element_by_name('xc_message')#xpath("//form/table/tbody/tr/td[1]/div/textarea")
    message_box.send_keys(message)
    send_button = browser.find_element_by_name('view_post')
    send_button.click()
def main():
    message = str(input('Enter message: '))
    filename = 'facebook_groups.csv'
    login(username, password)
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader: 
            group_link = 'https://mbasic.facebook.com/groups/' + row[0]     
            write_message(group_link, message)
            time.sleep(5)
if __name__ == __name__:
    main()
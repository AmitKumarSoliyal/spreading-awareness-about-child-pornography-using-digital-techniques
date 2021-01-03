# import dependencies
import http.cookiejar
import urllib.request
import requests
from bs4 import BeautifulSoup
from secrets import username, password, page_like_url, page_comment_url
import csv
import time
import argparse
from sys import argv
class facebookBot:
    facebook_url = 'https://mbasic.facebook.com'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    def __init__(self):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)
    def login(self, username, password):
        login_url = 'https://mbasic.facebook.com/login.php'
        payload = {
            'email' : username,
            'pass': password
        }
        login_data = urllib.parse.urlencode(payload).encode('utf-8')
        login_request = urllib.request.Request(login_url, login_data, headers = self.headers)
        login_response = urllib.request.urlopen(login_request)
        if login_response.status == 200:
            print('Login success')
        else:
            print('Login fail')
def main(self):

if __name__ == "__main__":
    main()
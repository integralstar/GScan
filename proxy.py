from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import Options
import requests
import pandas as pd
import time
import re


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')


def get_proxy_list():
    chromedriver = "/chromedriver/chromedriver"
    driver = webdriver.Chrome(chromedriver, options=chrome_options)

    print("cookie setting")
    time.sleep(7)

    s = HTMLSession()
    cookies = driver.get_cookies()
    driver.quit()

    for cookie in cookies:
        c = {cookie['name']: cookie['value']}
        s.cookies.update(c)

    base_url = 'http://spys.one/en/anonymous-proxy-list/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    data = {"xpp": "1", "xf1": "0", "xf2": "0", "xf4": "0", "xf5": "2"}
    result = s.post(base_url, data=data, headers=headers)
    soup = BeautifulSoup(result.content, 'html.parser')

    print(soup.get_text())

    proxy_list = []

    ports = {}
    script = soup.select_one("body > script")
    for row in script.text.split(";"):
        if "^" in row:
            line = row.split("=")
            ports[line[0]] = line[1].split("^")[0]

    trs = soup.select("tr[onmouseover]")

    for tr in trs:
        ip = ""
        port = ""

        # Get IP address
        e_ip = tr.select_one("font.spy14")

        # Get port number
        e_port = tr.select_one("script")

        if e_port is not None:
            re_port = re.compile(r'\(([a-zA-Z0-9]+)\^[a-zA-Z0-9]+\)')
            match = re_port.findall(e_port.text)
            for item in match:
                port = port + ports[item]
        else:
            continue

        # Get ip number
        if e_ip is not None:
            for item in e_ip.findAll('script'):
                item.extract()
            ip = e_ip.text
        else:
            continue

        # Get uptime value (%)
        tds = tr.select("td")
        is_skip = False
        for td in tds:
            e_pct = td.select_one("font > acronym")
            if e_pct is not None:
                pct = re.sub('([0-9]+)%.*', r'\1', e_pct.text)
                if not pct.isdigit():
                    is_skip = True
            else:
                continue

        if is_skip:
            continue

        proxy_list.append((ip + ":" + port, pct))

    proxy_list.sort(key=lambda element: int(element[1]), reverse=True)
    df = pd.DataFrame(proxy_list, columns=['proxy', 'pct'])
    df.drop('pct', axis=1, inplace=True)
    # save proxy list to file
    df.to_csv('proxy.csv', index=False)

    return df['proxy'].values.tolist()

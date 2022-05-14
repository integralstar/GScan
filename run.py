import json
import time
import random
import argparse
import schedule
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from collections import deque
from wsgiref.headers import Headers
from urllib.parse import quote_plus
from proxy import get_proxy_list
from tornetwork import use_tornetwork

# GOOGLE SEARCH API KEY & ENGINE ID
API_KEY = ['']
SEARCH_ENGINE = ['']

USER_AGENT = []

proxy_list = []
proxy_port = []


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', dest='domain', help='Domain name')
    options = parser.parse_args()
    return options


def proxy():
    csv = pd.read_csv('proxy.csv', names=[
                      'proxy', 'pct'], skiprows=1, encoding='CP949')
    return csv['proxy'].values.tolist()


def weekdays(date):
    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    day = date.weekday()
    q = deque(days)
    q.rotate(7 - int(day))
    result = list(q)
    return result


def scan(domain, start=1, end=73):

    for x in tqdm(range(start, end)):
        pattern = []
        pattern_file = './pattern/dork_' + str(x)+'.txt'

        print(pattern_file)

        # pattern files
        with open(pattern_file, 'r') as f:
            lines = f.readlines()

            for line in lines:
                pattern = "site:" + domain + " " + line
                print(pattern)
                time.sleep(random.randint(0, 7))

        # proxy setting for renewal
        proxy_list = get_proxy_list()

        for i in range(len(proxy_list)):
            if proxy_list[i].split(":")[1] == "80":
                proxy_port.append("HTTP")
            else:
                proxy_port.append("HTTPS")

        # 검색
        try:
            f = open("useragents.txt", "r")
            lines = f.readlines()

            for line in lines:
                # print(line)
                USER_AGENT.append(line.strip('\n').strip('\r'))

            f.close()

            headers = {
                'User-Agent': USER_AGENT[random.randint(0, 68)],
            }

            google_search_api_url = 'https://www.googleapis.com/customsearch/v1?key=' + \
                API_KEY[x] + '&cx=' + SEARCH_ENGINE[x] + \
                '&q={}'.format(quote_plus(pattern))

            response = requests.get(google_search_api_url, headers=headers, proxies={
                                    proxy_port[x]: proxy_list[x]})

            #print("response code : ", response.status_code)

            if response.status_code == 200:
                response_json = json.loads(response.text)

                if response_json['searchInformation']['totalResults'] != '0':
                    # 검색 결과가 존재 할 경우 패턴을 화면에 출력
                    print(pattern)
                    # 로그 파일 저장
                    filename = './log/log_' + time.time() + '.txt'
                    with open(filename, 'at+') as fd:
                        fd.write(pattern + '\n')

                        for x in response_json['items']:
                            # 구글에서 찾은 링크 주소 화면 출력
                            print(x['link'])
                            # 로그 파일 구글 해킹 결과 링크 저장
                            fd.write(x['link'] + '\n')

        except Exception as e:
            print("Google Search API fail log : ", google_search_api_url)
            print(e)

    return schedule.CancelJob


if __name__ == '__main__':

    options = get_arguments()

    if options.domain:
        domain = options.domain

    week = []
    week = weekdays(datetime.today())

    for x in week:
        if x == 'monday':
            schedule.every().monday.do(scan, domain, 1, 11)
        elif x == 'tuesday':
            schedule.every().tuesday.do(scan, domain, 11, 21)
        elif x == 'wednesday':
            schedule.every().wednesday.do(scan, domain, 21, 31)
        elif x == 'thursday':
            schedule.every().thursday.do(scan, domain, 31, 41)
        elif x == 'friday':
            schedule.every().friday.do(scan, domain, 41, 51)
        elif x == 'saturday':
            schedule.every().saturday.do(scan, domain, 51, 61)
        elif x == 'sunday':
            schedule.every().sunday.do(scan, domain, 61, 71)
            schedule.every().sunday.do(scan, domain, 71, 73)

    while True:
        schedule.run_pending()

        if not schedule.jobs:
            break

        time.sleep(60 * 60)

    print("Scanning finished...")

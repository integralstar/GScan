import json
import time
import random
import schedule
import requests
import pandas as pd
from tqdm import tqdm
from urllib.parse import quote_plus
from proxy import get_proxy_list
from tornetwork import use_tornetwork

# API_KEY LIST
API_KEY = ['']
SEARCH_ENGINE = ['']

proxy_list = []
proxy_port = []


def get_domain():
    domain = []
    # 도메인 리스트 파일
    with open("./domain_list/domain.txt", 'r') as fp:
        lines = fp.readlines()

        for line in lines:
            domain.append(line.strip('\n').strip('\r'))

    return domain


def proxy():
    csv = pd.read_csv('proxy.csv', names=[
                      'proxy', 'pct'], skiprows=1, encoding='CP949')
    return csv['proxy'].values.tolist()


def scan(domain, start=1, end=73):

    for x in tqdm(range(start, end)):
        pattern = []
        pattern_file = './pattern/dork_' + \
            str(x)+'.txt'

        print(pattern_file)

        # pattern files
        with open(pattern_file, 'r') as f:
            lines = f.readlines()

            for line in lines:
                pattern = "site:" + domain + " " + line
                print(pattern)
                time.sleep(random.randint(0, 7))

        # proxy setting renewal
        proxy_list = get_proxy_list()

        for i in range(len(proxy_list)):
            if proxy_list[i].split(":")[1] == "80":
                proxy_port.append("HTTP")
            else:
                proxy_port.append("HTTPS")

        # 검색
        try:
            google_search_api_url = 'https://www.googleapis.com/customsearch/v1?key=' + \
                API_KEY[x] + '&cx=' + SEARCH_ENGINE[x] + \
                '&q={}'.format(quote_plus(pattern))

            response = requests.get(google_search_api_url, proxies={
                                    proxy_port[x]: proxy_list[x]})

            #print("response code : ", response.status_code)

            if response.status_code == 200:
                response_json = json.loads(response.text)

                if response_json['searchInformation']['totalResults'] != '0':
                    # 검색 결과가 존재 할 경우 패턴을 화면에 출력
                    print(pattern)
                    # 로그 파일 저장
                    with open('./log/log.txt', 'at+') as fd:
                        fd.write(pattern + '\n')

                        for x in response_json['items']:
                            # 구글에서 찾은 링크 주소 화면 출력
                            print(x['link'])

                            fd.write(x['link'] + '\n')

        except Exception as e:
            print("Google Search API fail log : ", google_search_api_url)
            print(e)

    return schedule.CancelJob


if __name__ == '__main__':

    domain_list = []
    domain_list = get_domain()

    for domain in domain_list:
        schedule.every().sunday.do(scan, domain, 1, 11)
        schedule.every().monday.do(scan, domain, 11, 21)
        schedule.every().tuesday.do(scan, domain, 21, 31)
        schedule.every().wednesday.do(scan, domain, 31, 41)
        schedule.every().thursday.do(scan, domain, 41, 51)
        schedule.every().friday.do(scan, domain, 51, 61)
        schedule.every().saturday.do(scan, domain, 61, 71)
        schedule.every().saturday.do(scan, domain, 71, 72)

    while True:
        schedule.run_pending()
        if not schedule.jobs:
            break
        time.sleep(1)

    print("Finished...")

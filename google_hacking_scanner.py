import re
import csv
import sys
import json
import requests
import argparse

import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

from urllib.parse import quote_plus
from bs4 import BeautifulSoup as Soup

SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 465
SMTP_USER = ''
SMTP_PASSWORD = ''

def pattern_maker(domain):

    pattern_list = list()

    with open('./googledb.csv', newline='\n', encoding='utf-8') as f:
        pattern = csv.reader(f)
        
        for query in pattern:
            query = 'site:' + str(domain) + ' ' + str(query[0])
            pattern_list.append(query)

    return pattern_list

def mail_sender(query, message):

    try:
        msg = EmailMessage()
        msg['Subject'] = '제목 : 구글 검색 엔진에 노출된 패턴이 발견 되었습니다.'
        msg['From'] = ''
        msg['To'] = ''

        html = """\
            <html>
            <body>
                <p>발견된 결과</p><br><br>
                <p>사용된 패턴 : <strong>""" + query + """</strong></p><br>
                <p><strong>""" + message + """</strong></p><br>
                <p>감사합니다!</p>
            </body>
            </html>
        """
        # mail = MIMEText(html, "html")
        # msg.attach(mail)
        msg.set_content(html, subtype='html')

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            #smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(msg)        

    except Exception as e:
        print(e)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='GHDB Scanner')
    parser.add_argument('-d', '--domain', help='domain address')

    args = parser.parse_args()

    API_KEY = ''
    SEARCH_ENGINE = ''

    scan_pattern = list()

    if args.domain :
        scan_pattern = pattern_maker(args.domain)
    else:
        sys.exit()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }

    for index, query in enumerate(scan_pattern, start=1):
        google_search_api_url = 'https://www.googleapis.com/customsearch/v1?key=' + \
            API_KEY + '&cx=' + SEARCH_ENGINE + '&q={}'.format(quote_plus(query))

        print(index, google_search_api_url)

        if (index % 100) == 0 :
            time.sleep(24 * 60 * 60)

        response = requests.get(google_search_api_url, headers=headers)

        #print("response code : ", response.status_code)

        if response.status_code == 200:
            soup = Soup(response.text, 'html.parser')

            search_list = soup.find_all('div', attrs={'class': 'g'})

            try:
                for search in search_list:
                    # 컨텐츠 URL 꺼내기
                    a_href = search.find('a')['href']

                    if a_href :
                        print("found pattern : ", a_href)
                        mail_sender(query, a_href)
            except:
                traceback.print_exc()
import re
import csv
import ssl
import requests
import argparse
import traceback
from selenium import webdriver
from urllib.parse import quote_plus
from bs4 import BeautifulSoup as Soup


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', dest='query', help='GoogleDB query')
    parser.add_argument('-c', '--category',
                        dest='category', help='GoogleDB category')
    parser.add_argument('-k', '--keyword', dest='keyword', help='keyword')
    parser.add_argument('-d', '--domain', dest='domain', help='domain')
    parser.add_argument('-p', '--processes', dest='processes',
                        help='number of processes', default=1)
    parser.add_argument('-o', '--output', dest='output', help='output file')
    parser.add_argument('-v', '--verbose', dest='verbose', help='verbose mode',
                        action='store_true')

    options = parser.parse_args()
    return options


def pattern_maker(domain):
    pattern_list = []

    for row in pattern:
        row = 'site:' + domain + ' ' + row
        pattern_list.append(row)

    return pattern_list


def keyword_query(keyword=None, domain=None):

    pattern = []

    with open('googledb.csv', newline='\n', encoding='utf-8') as f:
        reader = csv.reader(f)
        for r in reader:

            row = ''.join(r)

            if keyword == 'php':
                prog = re.compile(r'^.*php.*', re.I)
                match1 = re.search(prog, row)
                match2 = re.search(r'^.*\.inc.*', row)
                match3 = re.search(r'^.*filetype:php.*', row)
                match4 = re.search(r'^.*ext:php.*', row)

                if match1 or match2 or match3 or match4:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'wordpress':
                match1 = re.search(r'^.*\.wp-.*', row)
                match2 = re.search(r'^.*\.wordpress.*', row)

                if match1 or match2:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'asp':
                match1 = re.search(r'^.*\.asp.*', row)
                match2 = re.search(r'^.*\.aspx.*', row)
                match3 = re.search(r'^.*ext:asp.*', row)
                match4 = re.search(r'^.*filetype:asp.*', row)

                if match1 or match2 or match3 or match4:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'jsp' or keyword == 'java':
                match0 = re.search(r'^.*\.jsp.*', row)
                match1 = re.search(r'^.*ext:jsp.*', row)
                match2 = re.search(r'^.*filetype:jsp.*', row)
                match3 = re.search(r'^.*filetype:java.*', row)
                match4 = re.search(r'^.*filetype:action.*', row)

                if match0 or match1 or match2 or match3 or match4:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'sql' or keyword == 'db' or keyword == 'database':
                match0 = re.search(r'^.*\.sql\s.*', row)
                match1 = re.search(r'^.*filetype:sql\s.*', row)
                match2 = re.search(r'^.*ext:sql\s.*', row)
                match3 = re.search(r'^.*ext:yml\s.*', row)
                match4 = re.search(r'^.*filetype:yml\s.*', row)
                match5 = re.search(r'^.*mysql.*', row)
                match6 = re.search(r'^.*ext:old.*', row)
                match7 = re.search(r'^.*filetype:old.*', row)
                match8 = re.search(r'^.*filetype:cnf\s.*', row)
                match9 = re.search(r'^.*filetype:myd\s.*', row)
                match10 = re.search(r'^.*filetype:mdb\s.*', row)
                match11 = re.search(r'^.*mongo.*', row)
                match12 = re.search(r'^.*sqlite_.*', row)

                if match0 or match1 or match2 or match3 or match4 or match5 or match6 or match7 or match8 or match9 or match10 or match11 or match12:
                    row = 'site:' + domain + ' ' + str(row)
                    pattern.append(row)

            elif keyword == 'ftp':
                match = re.search(r'^.*\.ftp.*', row)

                if match != None:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'http' or keyword == 'https':
                match = re.search(r'^.*\.http.*', row)

                if match != None:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'windows':
                match1 = re.search(r'^.*\.exe.*', row)
                match2 = re.search(r'^.*\.dll.*', row)
                match3 = re.search(r'^.*\.ini.*', row)
                match4 = re.search(r'^.*\.microsoft.*', row)
                match5 = re.search(r'^.*filetype:reg.*', row)

                if match1 or match2 or match3 or match4 or match5:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'python':
                match1 = re.search(r'^.*django.*', row)
                match2 = re.search(r'^.*(inurl:|intitle:).*\.py.*', row)
                match3 = re.search(r'^.*ext:py.*', row)
                match4 = re.search(r'^.*filetype:py.*', row)

                if match1 or match2 or match3 or match4:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'redis':
                match = re.search(r'^.*redis_.*', row)

                if match != None:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'perl':
                match1 = re.search(r'^.*inurl:perl.*', row)
                match2 = re.search(r'^.*filetype:pl\s.*', row)

                if match1 or match2:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'documents' or keyword == 'doc':
                match1 = re.search(r'^.*filtetype:hwp.*', row)
                match2 = re.search(r'^.*ext:hwp.*', row)
                match3 = re.search(r'^.*filetype:xls.*', row)
                match4 = re.search(r'^.*filetype:xlsx.*', row)
                match5 = re.search(r'^.*ext:xls.*', row)
                match6 = re.search(r'^.*ext:xlsx.*', row)
                match7 = re.search(r'^.*filetype:doc.*', row)
                match8 = re.search(r'^.*filetype:docx.*', row)
                match9 = re.search(r'^.*ext:doc.*', row)
                match10 = re.search(r'^.*ext:docx.*', row)

                if match1 or match2 or match3 or match4 or match5 or match6 or match7 or match8 or match9 or match10:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'pdf':
                match0 = re.search(r'^.*ext:pdf.*', row)
                match1 = re.search(r'^.*filetype:pdf.*', row)

                if match != None:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'txt':
                match0 = re.search(r'^.*ext:txt\s.*', row)
                match1 = re.search(r'^.*filetype:txt\s.*', row)

                if match0 or match1:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'log':
                match = re.search(r'^.*ext:log.*', row)

                if match != None:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'reg':
                match0 = re.search(r'^.*ext:reg.*', row)
                match1 = re.search(r'^.*filetype:reg.*', row)

                if match0 or match1:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'csv':
                match = re.search(r'^.*ext:csv.*', row)

                if match != None:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'cgi':
                match0 = re.search(r'^.*ext:cgi.*', row)
                match1 = re.search(r'^.*filetype:cgi.*', row)

                if match != None:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'env':
                match = re.search(r'^.*ext:env.*', row)

                if match != None:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'cache':
                match0 = re.search(r'^.*ext:cache.*', row)
                match1 = re.search(r'^.*filetype:cache.*', row)

                if match0 or match1:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'xml':
                match0 = re.search(r'^.*ext:xml.*', row)
                match1 = re.search(r'^.*filetype:xml.*', row)

                if match0 or match1:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

            elif keyword == 'password':
                match0 = re.search(r'^.*ext:password.*', row)
                match1 = re.search(r'^.*filetype:password.*', row)

                if match0 or match1:
                    row = 'site:' + domain + ' ' + row
                    pattern.append(row)

    pattern = list(set(pattern))

    return pattern


def description_show():
    print("1 : Footholds")
    print("2 : Files Containing Usernames")
    print("3 : Sensitives Directories")
    print("4 : Web Server Detection")
    print("5 : Vulnerable Files")
    print("6 : Vulnerable Servers")
    print("7 : Error Messages")
    print("8 : Files Containing Juicy Info")
    print("9 : Files Containing Passwords")
    print("10 : Sensitive Online Shopping Info")
    print("11 : Network or Vulnerability Data")
    print("12 : Pages Containing Login Portals")
    print("13 : Various Online Devices")
    print("14 : Advisories and Vulnerabilities")


def googlehacking_query(number):

    with open('google_hacking_db.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        custom_pattern = []

        for row in reader:
            if number == 0:
                description_show()
                break
            elif number == 1:
                if row['category_title'].rstrip() == 'Footholds':
                    custom_pattern.append(row['url_title'])
            elif number == 2:
                if row['category_title'].rstrip() == 'Files Containing Usernames':
                    custom_pattern.append(row['url_title'])
            elif number == 3:
                if row['category_title'].rstrip() == 'Sensitive Directories':
                    custom_pattern.append(row['url_title'])
            elif number == 4:
                if row['category_title'].rstrip() == 'Web Server Detection':
                    custom_pattern.append(row['url_title'])
            elif number == 5:
                if row['category_title'].rstrip() == 'Vulnerable Files':
                    custom_pattern.append(row['url_title'])
            elif number == 6:
                if row['category_title'].rstrip() == 'Vulnerable Servers':
                    custom_pattern.append(row['url_title'])
            elif number == 7:
                if row['category_title'].rstrip() == 'Error Messages':
                    custom_pattern.append(row['url_title'])
            elif number == 8:
                if row['category_title'].rstrip() == 'Files Containing Juicy Info':
                    custom_pattern.append(row['url_title'])
            elif number == 9:
                if row['category_title'].rstrip() == 'Files Containing Passwords':
                    custom_pattern.append(row['url_title'])
            elif number == 10:
                if row['category_title'].rstrip() == 'Sensitive Online Shopping Info':
                    custom_pattern.append(row['url_title'])
            elif number == 11:
                if row['category_title'].rstrip() == 'Network or Vulnerability Data':
                    custom_pattern.append(row['url_title'])
            elif number == 12:
                if row['category_title'].rstrip() == 'Pages Containing Login Portals':
                    custom_pattern.append(row['url_title'])
            elif number == 13:
                if row['category_title'].rstrip() == 'Various Online Devices':
                    custom_pattern.append(row['url_title'])
            elif number == 14:
                if row['category_title'].rstrip() == 'Advisories and Vulnerabilities':
                    custom_pattern.append(row['url_title'])

        return custom_pattern


def search(query, processes=1, output=None, verbose=False):
    """
    Search Google for query and return a list of links
    """
    links = []
    #context = ssl._create_unverified_context

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }

    url = "https://www.google.com/search?q={}".format(quote_plus(query))
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # print(response.text)
        soup = Soup(response.text, 'html.parser')

        search_list = soup.find_all('div', attrs={'class': 'g'})

        try:
            for search in search_list:
                # 컨텐츠 URL 꺼내기
                a_href = search.find('a')['href']
                print(a_href)

        except:
            traceback.print_exc()

        # soup = Soup(response.text, "html.parser")
        # results = soup.findAll("cite")

        # print("results : ", results)

        # for result in results:
        #     links.append(result.text)
        #     print(result.text)
    # return result


if __name__ == "__main__":

    pattern = []

    options = get_arguments()

    if options.query:
        search(options.query, int(options.processes))
        exit()

    elif options.keyword and options.domain:
        keyword = options.keyword
        domain = options.domain
        pattern = keyword_query(keyword, domain)
        if len(pattern) != 0:
            print("find", len(pattern), "keyword patterns.")

        for p in pattern:
            print(str(p))
            search(p, int(options.processes))
            print()

    elif options.category:
        category = options.category
        pattern = googlehacking_query(int(category))

        if len(pattern) != 0:
            print("find", len(pattern), "custom patterns.")

        for p in pattern:
            print(str(p))

    else:
        print("Please specify a query")
        exit()

    # for link in links:
    #     print(link)

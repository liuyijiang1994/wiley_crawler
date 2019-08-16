import requests

from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import random
import os

headers = {
    'Sec-Fetch-Mode': 'cors',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

abs_url = 'https://onlinelibrary.wiley.com/action/PB2showAjaxAbstract?isItemAbstract=true&doi='
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
         'December']
month = {m: k + 1 for k, m in enumerate(month)}
years = [1995 + i * 5 for i in range(5)]
doi_set = set()


def get_html(search_word, after_year, before_year, start_page, page_size, return_num=False):
    url = f'https://onlinelibrary.wiley.com/action/doSearch?AllField={search_word}&startPage={start_page}&pageSize={page_size}&AfterYear={after_year}&BeforeYear={before_year}&content=articlesChapters&countTerms=true&target=default'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        if return_num:
            soup = BeautifulSoup(response.text, 'lxml')
            num = soup.find('a', class_='search-result__nav__item active') \
                      .find('span').text.strip()[1:-1].replace(',', '')
            return num
        else:
            with open(f'html/{after_year}/{start_page}.html', 'w') as w:
                w.write(response.text)
    else:
        print('error', search_word, after_year, before_year, start_page, page_size)


def get_abs(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        abs = soup.find('div', class_='article-section__content en main').text.replace(
            'Copyright © 2004 John Wiley & Sons, Ltd.', '').strip()
        abs = abs.replace('\n', '. ').replace('   ', ' ').replace('   ', ' ') \
            .replace('  ', ' ').replace('  ', ' ').replace('. . ', '. ') \
            .replace('. . ', '. ').replace('. . ', '. ')
        return abs
    else:
        return ''


def parse_html(file_path):
    soup = BeautifulSoup(open(file_path), 'lxml')
    papers = soup.find_all('div', class_='item__body')
    for paper in papers:
        title = paper.find('a', class_='publication_title visitable')
        doi = title.get('href')[5:]
        abs = get_abs(abs_url + doi).strip()
        title = title.text
        year = paper.find('p', class_='meta__epubDate').text.strip()[-4:]
        print(doi)
        print(title)
        print(abs)
        print(year)


if __name__ == '__main__':
    for y in years:
        for filename in os.listdir(f'html/{y}'):
            print(filename)
# parse_html('html/2000_2005_page_0.html')
# get_abs('https://onlinelibrary.wiley.com/action/PB2showAjaxAbstract?doi=10.1002/3527605711.ch3&isItemAbstract=true')

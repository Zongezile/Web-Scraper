import requests
import os
from bs4 import BeautifulSoup

punctuation = '''!()-[]{};:'"\\,<>./?@#$%^&*_~'''

num_pages = int(input())
type_articles = str(input())

for page in range(num_pages):
    os.chdir(r'C:\Users\domik\PycharmProjects\Web Scraper3\Web Scraper\task')
    dir_name = 'Page_' + str(page + 1)
    os.mkdir(dir_name)
    if os.access(dir_name, os.F_OK):
        os.chdir(r'C:\Users\domik\PycharmProjects\Web Scraper3\Web Scraper\task\Page_' + str(page + 1))

    r = requests.get(
        'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page=' + str(page + 1))
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.find_all('article')

    for article in articles:
        current_type = article.find('span', {'data-test': 'article.type'}).text.strip()
        if current_type == type_articles:
            a = article.find('a', {'data-track-action': 'view article'})
            link = 'https://www.nature.com' + a.get('href')
            title = a.text
            for sign in title:
                if sign in punctuation:
                    title = title.replace(sign, "")
            new_title = title.translate(title.maketrans(" ", "_"))

            current_r = requests.get(link)
            current_soup = BeautifulSoup(current_r.content, 'html.parser')
            paragraphs = current_soup.select('.c-article-body p:not(.recommended__title), .c-article-body h2')

            file = open(f'{new_title}.txt', 'wb')
            for p in paragraphs:
                byte_paragraph = bytes(p.text + '\n', encoding='utf-8')
                file.write(byte_paragraph)
            file.close()

print('Saved all articles.')

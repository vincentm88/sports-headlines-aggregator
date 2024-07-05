import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse


def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def fetch_article_html(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print("Error:", e)

def parse_articles_from_html(url, html, main_selector, title_selector):
    articles = []
    soup = BeautifulSoup(html, 'html.parser')
    articles_list = soup.select(main_selector)
    if articles_list:
        for article in articles_list:
            if title_selector == '':
                initial_title = article.get_text().strip()
            else:
                if article.select_one(title_selector):
                    initial_title = article.select_one(title_selector).get_text().strip()
                else:
                    initial_title = ''

            if initial_title != '':
                href = article.get('href')
                if not href.startswith('http'):
                    href = get_base_url(url) + href

                articles.append({'title': initial_title, 'link': href})

        return articles
    else:
        print(f"no articles found")
        return None


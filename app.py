from flask import Flask, render_template
from scraper import load_config, fetch_article_html, parse_articles_from_html

app = Flask(__name__)


@app.route('/')
def index():
    articles = []
    config = load_config('config.json')

    for site, details in config['sites'].items():
        print(f"Retrieving content from {details['url']}")
        print(f"Using selector: {details['link-selector']}")
        html = fetch_article_html(details['url'])
        if html:
            article = parse_articles_from_html(details['url'], html, details['link-selector'], details['title-selector'])
        else:
            print(f"Failed to retrieve content from {details['url']}")
            
        if article:
            articles.extend(article)
    print(f"Retrieved {len(articles)} articles")
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)

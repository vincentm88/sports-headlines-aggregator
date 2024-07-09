
from flask_cors import CORS
from flask import Flask, render_template, jsonify
from scraper import load_config, fetch_article_html, parse_articles_from_html, fetch_open_graph_metadata

app = Flask(__name__)
articles = []

def fetch_articles():

    config = load_config('config.json')

    for site, details in config['sites'].items():
        print(f"Retrieving content from {details['url']}")
        print(f"Using selector: {details['link-selector']}")
        html = fetch_article_html(details['url'])
        if html:
            articles_data = parse_articles_from_html(details['url'], html, details['link-selector'], details['title-selector'])
            articles.extend(articles_data)
        else:
            print(f"Failed to retrieve content from {details['url']}")

    return articles


CORS(app)

@app.route('/')
def index():
    articles = fetch_articles()
    return render_template('index.html', articles=articles)

@app.route('/article')
def get_articles():
    fetch_articles()
    return jsonify(articles)
    
@app.route('/article/<int:index>')
def get_metadata(index):
    try:
        article = articles[index]
        metadata = fetch_open_graph_metadata(article['link'])
        if metadata:
            article.update(metadata)
        return jsonify(article)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
  app.run(debug=True)
  # app.run(host="0.0.0.0", port=5000)

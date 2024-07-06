from flask import Flask, render_template, jsonify
from scraper import load_config, fetch_article_html, parse_articles_from_html, fetch_open_graph_metadata

app = Flask(__name__)
articles = []

@app.route('/')
def index():
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

    return render_template('index.html', articles=articles)

@app.route('/metadata/<int:index>')
def get_metadata(index):
    try:
        article = articles[index]
        metadata = fetch_open_graph_metadata(article['link'])
        if metadata:
            article.update(metadata)
        return jsonify(article)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

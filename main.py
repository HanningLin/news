from newsapi import NewsApiClient
from flask import Flask, request, send_from_directory
from flask import render_template, jsonify
from flask_cors import *
from newsapi.newsapi_exception import NewsAPIException

from headlines_filter import *
from word_list_generator import *

app = Flask(__name__)
CORS(app)

newsapi = NewsApiClient(api_key='1c882845395c4dbd97bb44b90964ecc2')
# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(country='us', language='en', page_size=30)
top_headlines_cnn = newsapi.get_top_headlines(sources='cnn', language='en', page_size=30)
top_headlines_fox = newsapi.get_top_headlines(sources='fox-news', language='en', page_size=30)


# @app.route('/', methods=['GET'])
# def index():
#     return send_from_directory(app.config['static/'], 'index.html')


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/style.css', methods=['GET'])
def css():
    return send_from_directory('.','style.css')


@app.route('/api/headlines_card_json', methods=['GET'])
def api_headlines_card_json():
    return jsonify(h_filter(top_headlines, 5))


@app.route('/api/headlines_CNN_json', methods=['GET'])
def api_headlines_cnn_json():
    return jsonify(h_filter(top_headlines_cnn, 4))


@app.route('/api/headlines_FOX_json', methods=['GET'])
def api_headlines_fox_json():
    return jsonify(h_filter(top_headlines_fox, 4))


@app.route('/api/word_list', methods=['GET'])
def api_word_list():
    return jsonify(
        {'wordlist': generate_word_list(newsapi.get_top_headlines(country='us', language='en', page_size=100))})


@app.route('/api/source', methods=['GET'])
def api_source():
    name = request.args.get('category')
    # print("Catagory from front end is {}".format(name.lower()))
    if name.lower() == "all":
        sources = newsapi.get_sources(language='en')
    else:
        sources = newsapi.get_sources(category=name.lower(), language='en')
    # print(sources)
    return jsonify(sources)


@app.route('/api/search_news', methods=['GET'])
def api_search_news():
    keyword = request.args.get('keyword').lower()
    date_from = request.args.get('dateFrom')
    date_to = request.args.get('dateTo')
    category_ = request.args.get('category').lower()
    source = request.args.get('source').lower()
    date1 = datetime.datetime.strptime(date_from, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date_to, "%Y-%m-%d")
    # today = datetime.date.today().strptime(date_to, "%Y-%m-%d")
    if date1 > date2:
        return jsonify({'status': 'error', 'message': 'Incorrect time'})
    try:
        if category_ == "all":
            if source == 'all':
                print("q = {}".format(keyword))
                headlines = newsapi.get_everything(language='en', page_size=30, q=keyword, from_param=date_from,
                                                   to=date_to, sort_by='publishedAt')
            else:
                print("q = {}; source = {}".format(keyword, source))
                headlines = newsapi.get_everything(language='en', page_size=30, q=keyword, sources=source,
                                                   from_param=date_from, to=date_to, sort_by='publishedAt')
        else:
            if source == 'all':
                print("q = {}; category = {}".format(keyword, category_))
                source_temp = newsapi.get_sources(category=category_, language='en')
                print(source_temp)
                source_str = ''
                for x in source_temp['sources']:
                    source_str += source_temp['sources'][0]['id']
                    source_str += ','
                source_str = source_str[0:len(source_str) - 1]
                print(source_str)
                headlines = newsapi.get_everything(language='en', page_size=30, q=keyword, sources=source_str,
                                                   from_param=date_from,
                                                   to=date_to, sort_by='publishedAt')
            else:
                print("q = {}; source = {}; category = {}".format(keyword, source, category_))
                headlines = newsapi.get_everything(language='en', page_size=30, q=keyword, sources=source,
                                                   from_param=date_from, to=date_to, sort_by='publishedAt')
        res = jsonify(search_filter(headlines))
        # print("res is {}".format(res))
        return res
    except NewsAPIException as e:
        return jsonify(e.get_exception())


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    images = []
    page = int(request.args.get('page', 0))
    keyword = ''

    if request.method == 'POST':
        keyword = request.form['keyword']
        page = 0
    else:
        keyword = request.args.get('keyword', '')

    if keyword:
        params = {
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'json': 1,
            'tags': keyword,
            'limit': 20,
            'pid': page
        }
        res = requests.get('https://safebooru.org/index.php', params=params)
        if res.status_code == 200:
            try:
                data = res.json()
                images = ['https:' + post['file_url'] for post in data if 'file_url' in post]
            except:
                images = []

    return render_template('index.html', images=images, keyword=keyword, page=page)

import webbrowser

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)


from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # List to store image URLs
    images = []

    # Get current page index from URL (defaults to 0 if not present)
    page = int(request.args.get('page', 0))

    # Keyword is either from POST (new search) or GET (pagination)
    keyword = ''
    if request.method == 'POST':
        keyword = request.form['keyword']   # New search input from user
        page = 0                            # Reset to first page
    elif request.method == 'GET':
        keyword = request.args.get('keyword', '')  # Keep keyword when paging

    # Only search if a keyword is provided
    if keyword:
        # Danbooru-style Safebooru API parameters
        params = {
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'json': 1,               # Return results in JSON
            'tags': keyword,         # Tag(s) to search
            'limit': 20,             # Images per page
            'pid': page              # Page index for pagination
        }

        # Make a GET request to Safebooru API
        response = requests.get('https://safebooru.org/index.php', params=params)

        if response.status_code == 200:
            data = response.json()

            # Extract image URLs from the JSON response
            images = [
                'https:' + post['file_url']
                for post in data
                if 'file_url' in post
            ]

    # Render the page with images, keyword, and current page
    return render_template('index.html',
                           images=images,
                           keyword=keyword,
                           page=page)

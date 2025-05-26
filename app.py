from flask import Flask, render_template, request
import requests
import webbrowser

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get search keyword and page number from the URL query
 if request.method == 'POST':
    keyword = request.form.get('keyword', '')
    page = 0  # Reset to first page on new search
 else:
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 0))

    # Set up API request parameters for Safebooru
    params = {
        'page': 'dapi',      # Required by the API
        's': 'post',         # Means we want post/image data
        'q': 'index',        # Request index (search)
        'json': 1,           # JSON response
        'tags': keyword,     # User's search keyword
        'limit': 20,         # 20 images per page
        'pid': page          # Which page number to load
    }

    # Make the HTTP request to Safebooru
    res = requests.get('https://safebooru.org/index.php', params=params, headers={"Accept": "application/json"})

    # If request was successful
    if res.status_code == 200:
        try:
            data = res.json()
            # Safebooru image URLs need to be built manually
            images = [
                f"https://safebooru.org/images/{post['directory']}/{post['image']}"
                for post in data if 'image' in post and 'directory' in post
            ]
        except Exception as e:
            print(f"Error: {e}")
            images = []
    else:
        images = []

    # Render the HTML template
    return render_template('index.html', images=images, keyword=keyword, page=page)

# Auto open browser on startup
if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)


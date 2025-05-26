from flask import Flask, render_template, request  # Import Flask framework tools
import requests  # To make HTTP requests to Safebooru API

app = Flask(__name__)  # Create Flask app instance

@app.route('/', methods=['GET', 'POST'])  # Define homepage route, accepts form GET and POST
def index():
    images = []  # Initialize empty list to hold image URLs

    # If the user submitted the form (POST request)
    if request.method == 'POST':
        keyword = request.form['keyword']  # Get the search tag entered by user

        # Parameters for Safebooru API request
        params = {
            'page': 'dapi',     # Use Danbooru API interface (Safebooru supports this)
            's': 'post',        # Search posts
            'q': 'index',       # List posts
            'json': 1,          # Request JSON response format
            'tags': keyword,    # Use the user input as search tags
            'limit': 20         # Number of posts to return
        }

        # Send GET request to Safebooru API with parameters
        response = requests.get('https://safebooru.org/index.php', params=params)

        # If the response is successful
        if response.status_code == 200:
            data = response.json()  # Parse the JSON data

            # Extract image URLs from each post if available
            images = [post['file_url'] for post in data if 'file_url' in post]

    # Render the HTML template, passing the image URLs to it
    return render_template('index.html', images=images)

# Run the Flask app in debug mode for easier troubleshooting
if __name__ == '__main__':
    app.run(debug=True)

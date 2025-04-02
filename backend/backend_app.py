"""
This is a simple Flask application that provides a
RESTful API for managing blog posts.

It includes endpoints for creating, retrieving (sorting,
pagination), updating, deleting, and searching for posts.

The application uses Flask-CORS for Cross-Origin Resource Sharing,
in this case the backend runs in Codio and the frontend in localhost.

It also uses Flask-Limiter for rate limiting to prevent abuse,
currently set to 10 requests per minute.

The application serves a Swagger UI for API documentation
and testing, which is available at the /api/docs endpoint.

The API supports versioning through the Accept header,
allowing clients to specify the desired version of the API

"""
from docutils.nodes import author
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint
import logging
import datetime
import webbrowser

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
limiter = Limiter(app=app, key_func=get_remote_address) # Rate limiting
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='my_log_file.log')


# swagger endpoint e.g. HTTP://localhost:5002/api/docs
SWAGGER_URL="/api/docs"
API_URL="/static/masterblog.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Masterblog API'})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post.",
     "author": "Your Name", "date": "28-02-2025"},
    {"id": 2, "title": "Second post", "content": "And this is the second post.",
     "author": "Your Name", "date": "01-03-2025"}
]


@app.route('/api/posts', methods=['GET', 'POST'])
@limiter.limit("10/minute")
def get_posts():
    """
    Handles GET and POST requests for the /api/posts
    endpoint. Logs the requests.

    * If the request is POST, it creates a new post in the database.
    It expects a JSON payload with the post data (title, content, author).
    It assigns a new ID to the post, adds the current date,
    and appends it to the list of posts.

    * If the request is GET, it retrieves all posts.
    Logs the request and returns a list of posts in JSON format.
    Optionally, it can filter posts by title, content or author in the query,
    in alphabetical order, also optionally in ascending or descending
    order. For example: .../api/posts?sort=title&direction=desc
    Optionally, it can paginate the results with page and limit.
    For example: .../api/posts?page=1&limit=10
    It also supports versioning through the Accept header,
    allowing clients to specify the desired version of the API response
    (currently v1 default, this feature is just to learn how to implement it).

    :payload new_post: A JSON payload with the new post data
        {"title": "New Title",
        "content": "New Content",
        "author": "New Author"}
    :return: A list of posts or a newly created post, or an error message,
    along with the appropriate HTTP status code.
    """
    if request.method == 'POST':
        app.logger.info('POST request received for /api/posts')
        new_post = request.get_json()
        if (not new_post or 'title' not in new_post
                or 'content' not in new_post
                or 'author' not in new_post):
            return jsonify({"error": "Invalid post data"}), 400

        ids = [post["id"] for post in POSTS]
        new_post['id'] = max(ids) + 1 if ids else 1

        date = datetime.datetime.now().strftime('%d-%m-%Y')
        new_post['date'] = date

        POSTS.append(new_post)
        return jsonify(new_post), 201

    elif request.method == 'GET':
        app.logger.info('GET request received for /api/posts')

        accept_header = request.headers.get('Accept')
        posts = POSTS[:]

        sort = request.args.get('sort')
        direction = request.args.get('direction')
        if sort:
            if sort == 'title':
                posts = sorted(posts, key=lambda post: post['title'].lower())
            elif sort == 'content':
                posts = sorted(posts, key=lambda post: post['content'].lower())
            elif sort == 'author':
                posts = sorted(posts, key=lambda post: post['author'].lower())
            else:
                return jsonify({"error": "Invalid sort parameter"}), 400

            if direction:
                if direction == 'desc':
                    posts = posts[::-1]
                ## Since the default is ascending, but the instructions
                ## explicitly say it should accept either asc or desc,
                ## this is the way I think it should be handled
                elif direction != 'asc':
                    return (jsonify({"error": "Invalid direction parameter"}),
                            400)

        page = int(request.args.get('page', 1))
        if page:
            limit = int(request.args.get('limit', 10))
            start_index = (page - 1) * limit
            end_index = start_index + limit
            posts = posts[start_index:end_index]

        ## For now I implemented the versioning for learning purposes
        if ('application/vnd.myapi.v1+json' in accept_header
                    or accept_header == 'application/json'):
            return jsonify(posts), 200
        elif 'application/vnd.myapi.v2+json' in accept_header:
            posts_v2 = [dict(post, version='v2') for post in posts]
            return jsonify(posts_v2), 200

        return jsonify(posts), 200


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Handles DELETE requests for the /api/posts/<int:post_id> endpoint.

    Logs the request and deletes the post with the specified ID.
    Checks if there is one less post in the database.

    :param post_id: Required post ID to delete as an integer.
    :return: A json response with a success message or an error message,
    along with the appropriate HTTP status code.
    """
    app.logger.info('DELETE request received for /api/posts/<int:post_id>')

    global POSTS
    initial_length = len(POSTS)
    POSTS = [post for post in POSTS if post.get('id') != post_id]

    if len(POSTS) < initial_length:
        return jsonify({"message": f"Post with id {post_id} "
                            f"has been deleted successfully."}), 200
    else:
        return jsonify({"error": "Post not found: please check the ID"}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Handles PUT requests for the /api/posts/<int:post_id> endpoint.

    Logs the request, checks if the post exists and updates its content.

    :param post_id: Required post ID to update as an integer.
    :payload new_content: JSON payload with the new content for the post.
        {"title": "New Title",
        "content": "New Content",
        "author": "New Author",
        "date": "New Date"}
    :return: The updated post in JSON format or an error message,
    along with the appropriate HTTP status code.
    """
    app.logger.info('PUT request received for /api/posts/<int:post_id>')

    global POSTS
    post = [post for post in POSTS if post.get('id') == post_id]

    if not post:
        return jsonify({"error": "Post not found: please check the ID"}), 404

    post_to_update = post[0]
    new_content = request.get_json()

    if new_content:
        if 'title' in new_content:
            post_to_update['title'] = new_content['title']
        if 'content' in new_content:
            post_to_update['content'] = new_content['content']
        if 'author' in new_content:
            post_to_update['author'] = new_content['author']
        if 'date' in new_content:
            post_to_update['date'] = new_content['date']

    for item, post in enumerate(POSTS):
        if post['id'] == post_id:
            post.update(post_to_update)
            break

    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts by title, content, author or date.

    Logs the request and filters the posts based on the search term.
    For example: .../api/posts/search?title=First
    :return: A list of posts that match the search term.
    """
    app.logger.info('GET request received for /api/posts/search')

    title = request.args.get('title', '')
    content = request.args.get('content', '')
    author = request.args.get('author', '')
    date = request.args.get('date', '')

    filtered_posts = []
    if title:
        filtered_posts = [post for post in POSTS if title.lower()
                          in post['title'].lower()]
    elif content:
        filtered_posts = [post for post in POSTS if content.lower()
                          in post['content'].lower()]
    elif author:
        filtered_posts = [post for post in POSTS if author.lower()
                          in post['author'].lower()]
    elif date:
        filtered_posts = [post for post in POSTS if date.lower()
                          in post['date'].lower()]

    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5002/api/docs')
    app.run(host="0.0.0.0", port=5002, debug=True)

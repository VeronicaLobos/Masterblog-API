"""
This is a simple Flask application that provides a
RESTful API for managing blog posts.

It includes endpoints for creating, retrieving (sorting,
pagination), updating, deleting, and searching for posts.

"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
limiter = Limiter(app=app, key_func=get_remote_address) # Rate limiting

# swagger endpoint e.g. HTTP://localhost:5002/api/docs
SWAGGER_URL="/api/docs"
API_URL="/static/masterblog.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Masterblog API'})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
@limiter.limit("10/minute")
def get_posts():
    """
    Handles GET and POST requests for the /api/posts
    endpoint.

    If the request is POST, it creates a new post in the database.

    If the request is GET, it retrieves all posts.
    Optionally, it can filter posts by title or content in the query,
    in alphabetical order, also optionally in ascending or descending
    order. For example: .../api/posts?sort=title&direction=desc
    Optionally, it can paginate the results with page and limit.
    :return: A list of posts or a newly created post.
    """
    if request.method == 'POST':
        # Create a new post from the request data
        new_post = request.get_json()
        if not new_post or 'title' not in new_post or 'content' not in new_post:
            return jsonify({"error": "Invalid post data"}), 400

        # Assign a new ID to the post
        ids = [post["id"] for post in POSTS]
        new_post['id'] = max(ids) + 1 if ids else 1

        # Add the new post to the posts list
        POSTS.append(new_post)
        return jsonify(new_post), 201

    elif request.method == 'GET':
        accept_header = request.headers.get('Accept')
        posts = POSTS[:]

        sort = request.args.get('sort')
        direction = request.args.get('direction')
        # Sort posts by title or content in alphabetical order
        if sort:
            if sort == 'title':
                posts = sorted(posts, key=lambda post: post['title'].lower())
            elif sort == 'content':
                posts = sorted(posts, key=lambda post: post['content'].lower())
            else:
                return jsonify({"error": "Invalid sort parameter"}), 400

            # Reverse the order if direction is specified
            if direction:
                if direction == 'desc':
                    posts = posts[::-1]
                ## Since the default is ascending, but the instructions
                ## explicitly say it should accept asc or desc, this is
                ## the way I think it should be handled
                elif direction != 'asc':
                    return (jsonify({"error": "Invalid direction parameter"}),
                            400)

        # Paginate the results
        page = int(request.args.get('page', 1))
        if page:
            limit = int(request.args.get('limit', 10))

            start_index = (page - 1) * limit
            end_index = start_index + limit

            posts = posts[start_index:end_index]

        if ('application/vnd.myapi.v1+json' in accept_header
                    or accept_header == 'application/json'):
            return jsonify(posts)
        elif 'application/vnd.myapi.v2+json' in accept_header:
            posts_v2 = [dict(post, version='v2') for post in posts]
            return jsonify(posts_v2)

        return jsonify(posts)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Find the post by ID and exclude it from the list
    global POSTS
    initial_length = len(POSTS)
    POSTS = [post for post in POSTS if post.get('id') != post_id]

    # Check if the post was deleted
    if len(POSTS) < initial_length:
        return jsonify({"message": f"Post with id {post_id} "
                            f"has been deleted successfully."}), 200
    else:
        return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    # Find the post by ID
    global POSTS
    post = [post for post in POSTS if post.get('id') == post_id]

    # If it doesn't exist, return an error
    if not post:
        return jsonify({"error": "Post not found"}), 404

    post_to_update = post[0]
    new_content = request.get_json()

    if new_content:
        # The title and content are optional
        if 'title' in new_content:
            post_to_update['title'] = new_content['title']
        if 'content' in new_content:
            post_to_update['content'] = new_content['content']

    # Update the post in the list
    for item, post in enumerate(POSTS):
        if post['id'] == post_id:
            post.update(post_to_update)
            break

    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts by title or content.
    :return: A list of posts that match the search term.
    """
    # Get the search term from the query parameters
    title = request.args.get('title', '')
    content = request.args.get('content', '')
    filtered_posts = []
    # Filter the posts based on the search term
    if title:
        filtered_posts = [post for post in POSTS if title.lower()
                          in post['title'].lower()]
    elif content:
        filtered_posts = [post for post in POSTS if content.lower()
                          in post['content'].lower()]

    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
limiter = Limiter(app=app, key_func=get_remote_address)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
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

    return jsonify(POSTS)


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

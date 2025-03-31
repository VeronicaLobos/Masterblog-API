from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

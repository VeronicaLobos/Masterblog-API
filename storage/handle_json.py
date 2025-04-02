"""
A simple module for reading and writing in a JSON database.
"""

import json
import os

class HandleJson():
    def __init__(self, file_path):
        self.file_path = file_path


    @property
    def load_posts_from_json(self):
        """
        Loads the posts from the database.

        If the file with the designated path doesn't exist,
        it creates one with example data (a list of dicts).

        Loads the data stored in the database and returns it.

        Handles errors like FileNotFoundError and JSONDecodeError
        by returning an empty list.
        """
        example_blog_posts = [
            {
                "title": "First post",
                "content": "This is the first post.",
                "author": "Your Name",
                "id": 1,
                "date": "2025-02-28"
            },
            {
                "title": "Second post",
                "content": "And this is the second post.",
                "author": "Your Name",
                "id": 2,
                "date": "2025-03-31"
            }
]

        try:
            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w', encoding='utf-8') as handle:
                    json.dump(example_blog_posts, handle, indent=4)

            with open(self.file_path, 'r', encoding='utf-8') as handle:
                return json.load(handle)

        except FileNotFoundError as e:
            print(e)
        except json.JSONDecodeError as e:
            print(e)
        return []


    def save_posts_to_json(self, updated_posts):
        """
        Receives a list of dictionaries and saves it to the database.
        """
        with open(self.file_path, 'w', encoding='utf-8') as handle:
            json.dump(updated_posts, handle, indent=4)
# Masterblog API, a CSR web application

In this school project, I created a simple blog application using Flask.
The front-end app CSR was provided. Currently working on completing the REST API with UPDATE and DELETE methods.

<img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/python.png" alt="Python" title="Python"/><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/pycharm.png" alt="PyCharm" title="PyCharm"/>
<img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/flask.png" alt="Flask" title="Flask"/>
<img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/postman.png" alt="Postman" title="Postman"/>

The objective was to learn the basics of creating an API with Flask and to understand how to handle CRUD operations.
Also learned how to create documentation for the API using Swagger UI.

<img width="597" alt="Screenshot 2025-04-02 at 10 15 52" src="https://github.com/user-attachments/assets/2ee22d1d-252d-4a74-891b-59483b6eef9b" />


The basic functionality includes:
-   Creating new blog posts
-   Viewing all blog posts
-   Updating existing blog posts by ID
-   Deleting blog posts by ID
-   Searching for blog posts by title, content, author, or date

## Tech Stack

*   **Flask:** This is a really cool Python framework that makes building web applications much easier.
*   **JSON:** This is a way to store data in a structured format. I use it to save the blog posts.
*   **Python:** This is the programming language that makes everything work.

## Backend API

The backend API is built using Flask and provides endpoints for creating, reading, updating, and deleting blog posts.
The API is designed to be simple and easy to use, with clear documentation for each endpoint.

### Key Features of the Backend app

-  **Route:** Direct users to different Endpoints.
-  **CRUD Operations:** Create, Read, Update, and Delete data.
-  **Rate Limiting:** Limit the number of requests to the API.
-  **CORS:** Allow cross-origin requests.
-  **Swagger UI:** Provides a user-friendly interface for testing the API.
-  **Documentation:** Clear documentation for each endpoint.
-  **Pagination:** Display a limited number of posts per page.
-  **Filtering:** Filter posts by title, content, author, or date.
-  **Error Handling:** The app provides feedback if something goes wrong.
-  **Unique IDs:** Each post has a unique ID for easy tracking.
-  **Data Persistence:** Posts are saved in a JSON file.
-  **OOP:** A class dedicated to serialize and deserialize data to and from the JSON file.  Designed for maintainability and better project organization.  In the future another module could handle other file formats like CSV.
-  **Logging:** Log all requests to the API.
-  **Versioning:** Version the API to allow for future changes without breaking existing functionality. Still in progress.

### API Endpoints

-  **GET /docs**: View the API documentation 
-  **GET /posts**: Retrieve all blog posts
-  **POST /posts**: Create a new blog post
-  **PUT /posts/<id>**: Update an existing blog post by ID
-  **DELETE /posts/<id>**: Delete a blog post by ID
-  **GET /posts/like/search**: Search for blog posts by title, content, author or date

While the API is functional, it is still a work in progress. I plan to add more features and improve the existing ones in the future, in particular completing the front end app.
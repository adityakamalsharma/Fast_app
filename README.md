# Fast_app
## FastAPI Authentication with SQLAlchemy

This is a simple and robust API for user authentication and management built with FastAPI. It demonstrates a secure and persistent user system using JWT (JSON Web Tokens) for authentication and SQLAlchemy for database integration.
Features

    User Registration: Securely create new user accounts with password hashing.

    JWT-based Authentication: Issue and validate JSON Web Tokens for secure access to protected endpoints.

    SQLAlchemy ORM: Persist user data in a database using a powerful Object-Relational Mapper.

    Dependency Injection: Utilize FastAPI's dependency injection system to manage database sessions and user authentication.

    ```
    ---
    

## Prerequisites

Before you begin, ensure you have the following installed:

    Python 3.8+

    pip (Python package installer)

--- 

## Installation

    Clone the repository:

    git clone https://github.com/adityakamalsharma/Fast_app.git
    cd Fast_app

    Create and activate a virtual environment:

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate

    Install the dependencies:
    The project uses a requirements.txt file to manage its dependencies.

    pip install -r requirements.txt


---

## How to Run the Application

The application can be run using uvicorn, a lightning-fast ASGI server.

    Run the server:

    uvicorn main:app --reload

    The --reload flag will automatically restart the server whenever you make changes to the code.

    Access the API Documentation:
    Once the server is running, you can access the interactive API documentation (provided by FastAPI) at http://127.0.0.1:8000/docs.


---

## API Endpoints

The API has three main endpoints that manage the user authentication flow:

* POST /register: New users can create an account by sending a POST request to this endpoint with their username, email, full name, and password. The password is then securely hashed and stored in the database.

* POST /token: Existing users can get an access token by sending a POST request with their username and password. This endpoint validates the credentials and returns a signed JSON Web Token (JWT).

*  GET /users/me: This is a protected endpoint. To access it, a user must provide a valid JWT in the Authorization header. This endpoint decodes the token, authenticates the user, and returns their profile information.
---

## Project Structure

For simplicity, all the code is contained within a single file, main.py.

* main.py: This file contains the entire FastAPI application, including the Pydantic models for data validation, the SQLAlchemy models for database schema, and all the API endpoints for authentication and user data.


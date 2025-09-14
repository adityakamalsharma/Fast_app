# Fast_app
## FastAPI Authentication with SQLAlchemy

This is a simple and robust API for user authentication and management built with FastAPI. It demonstrates a secure and persistent user system using JWT (JSON Web Tokens) for authentication and SQLAlchemy for database integration.
Features

    User Registration: Securely create new user accounts with password hashing.

    JWT-based Authentication: Issue and validate JSON Web Tokens for secure access to protected endpoints.

    SQLAlchemy ORM: Persist user data in a database using a powerful Object-Relational Mapper.

    Dependency Injection: Utilize FastAPI's dependency injection system to manage database sessions and user authentication.

    

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

---

## Testing the API

This section provides instructions on how to set up and test the secure API endpoints using curl.

### 1. Prerequisites

Before you begin, make sure you have Python installed. Then, install the necessary libraries using pip:


```
   pip install -r requirements.txt
```  



### 2. Running the Application

  Save the provided code as secure_api.py.

   Run the application from your terminal using uvicorn:
    ```
    
    uvicorn secure_api:app --reload

    ```
    
 The API will now be running and accessible at http://127.0.0.1:8000. The interactive API documentation (Swagger UI) will also be available at http://127.0.0.1:8000/docs.

### 3. Testing Endpoints with curl

Follow these steps in order to test the API's functionality.

* Step 1: Register a New User

First, register a new user by sending a 

POST request to the /register endpoint. 

```
curl -X POST "http://127.0.0.1:8000/register" \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "email": "test@example.com", "full_name": "Test User", "password": "aStrongPassword123"}'
```

You should receive a JSON response confirming the user's creation (without the password).

* Step 2: Log In to Get a JWT

Next, authenticate the user to receive a JSON Web Token (JWT). Send the 

username and password as form data to the /token endpoint (which functions as the login route). 

```
curl -X POST "http://127.0.0.1:8000/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=testuser&password=aStrongPassword123"
```

The response will contain your access_token. It will look something like this:
JSON
```

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Copy the long string value of the access_token. For convenience in the next step, you can save it to an environment variable:
```

export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

* Step 3: Access a Protected Route

Finally, use the obtained JWT to access a protected endpoint, such as 

/users/me/ (which corresponds to the /profile requirement).  The token must be included in the 

Authorization header.
```

curl -X GET "http://127.0.0.1:8000/users/me/" \
-H "Authorization: Bearer $TOKEN"
```


If the token is valid, you will receive the user's profile information as a JSON response:

```
JSON

{
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "disabled": false
}
```

If you try to access this endpoint without a token or with an invalid/expired one, you will receive a 401 Unauthorized error.

---

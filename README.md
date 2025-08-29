# Fast_app
FastAPI Authentication with SQLAlchemyThis is a simple and robust API for user authentication and management built with FastAPI. It demonstrates a secure and persistent user system using JWT (JSON Web Tokens) for authentication and SQLAlchemy for database integration.FeaturesUser Registration: Securely create new user accounts with password hashing.JWT-based Authentication: Issue and validate JSON Web Tokens for secure access to protected endpoints.SQLAlchemy ORM: Persist user data in a database using a powerful Object-Relational Mapper.Dependency Injection: Utilize FastAPI's dependency injection system to manage database sessions and user authentication.PrerequisitesBefore you begin, ensure you have the following installed:Python 3.8+pip (Python package installer)InstallationClone the repository:git clone <your-repository-url>
cd <your-project-directory>
Create and activate a virtual environment:# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
py -m venv venv
venv\Scripts\activate
Install the dependencies:The project uses a requirements.txt file to manage its dependencies.pip install -r requirements.txt
How to Run the ApplicationThe application can be run using uvicorn, a lightning-fast ASGI server.Run the server:uvicorn main:app --reload
The --reload flag will automatically restart the server whenever you make changes to the code.Access the API Documentation:Once the server is running, you can access the interactive API documentation (provided by FastAPI) at http://127.0.0.1:8000/docs.API EndpointsEndpointMethodDescription/registerPOSTRegister a new user./tokenPOSTAuthenticate a user and get an access token./users/meGETGet the current authenticated user's profile./users/me/itemsGETGet a list of items owned by the current user. (Example)Project StructureFor simplicity, all the code is contained within a single file, main.py.main.py: This file contains the entire FastAPI application, including the Pydantic models for data validation, the SQLAlchemy models for database schema, and all the API endpoints for authentication and user data.To understand the internal logic and workflow, please refer to the auth_flow.txt and auth_guide.md files, which explain the data flow and the step-by-step authentication process in detail.

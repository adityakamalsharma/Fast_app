from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import select

# Configuration
SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup
# This is a SQLite database file that will be created in the project directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# create_engine is the primary entry point to the database, configuring the connection.
# The `connect_args` are needed for SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# `sessionmaker` creates a class that will be our database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# `declarative_base` returns a base class that our ORM models will inherit from.
Base = declarative_base()

# Database model for the User table
class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)

# Create the database tables
# This function will be called on startup to create all tables defined with `Base`.
def create_db_tables():
    Base.metadata.create_all(bind=engine)

# Pydantic models for data validation (separate from ORM models)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: str

# Password hashing context and OAuth2 scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    on_startup=[create_db_tables]
)

# Dependency to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions
def verify_password(plain_password, hashed_password):
    """Verifies a plain password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)

def get_user_from_db(db: Session, username: str):
    """Retrieves a user from the database."""
    return db.scalars(select(UserORM).filter_by(username=username)).first()

def authenticate_user(db: Session, username: str, password: str):
    """Authenticates a user with a given username and password."""
    user = get_user_from_db(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    # Convert the ORM model to a Pydantic model for consistency
    return UserInDB(**user.__dict__)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get the current user
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Decodes the JWT token and returns the corresponding user."""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = get_user_from_db(db, username=token_data.username)
    if user is None:
        raise credential_exception
    # Convert ORM model to Pydantic model
    return UserInDB(**user.__dict__)

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    """Checks if the user is active."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# API Endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticates a user and returns a JWT access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=User)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user.
    - Hashes the password before storing it.
    - Returns a HTTPException if the username or email already exists.
    """
    # Check if user already exists
    existing_user = get_user_from_db(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    # Create the user in the database
    new_user_orm = UserORM(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        disabled=False
    )
    
    db.add(new_user_orm)
    db.commit()
    db.refresh(new_user_orm)
    
    # Return the new user object without the hashed password
    return User(**new_user_orm.__dict__)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Returns the current logged-in user's information."""
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """Returns a list of items for the current user (example endpoint)."""
    return [{"item_id": 1, "owner": current_user}]

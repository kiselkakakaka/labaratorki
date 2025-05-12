from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), label="static")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://isp_r_Morozova:12345@77.91.86.135/isp_r_Morozova")
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Client(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50), index=True)  
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(100))
    disabled = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    client_id: str
    email: EmailStr
    full_name: str | None = None
    access_key: str

class UserUpdate(BaseModel):
    client_id: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    access_key: str | None = None
    disabled: bool | None = None

class UserResponse(BaseModel):
    id: int
    client_id: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool | None = None
    class Config:
        from_attributes = True

class ClientInDB(UserResponse):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(access_key: str) -> str:
    return pwd_context.hash(access_key)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, client_id: str, access_key: str):
    client = get_user_by_username(db, client_id)
    if not client:
        logger.error("Client not found")
        return False
    if not verify_password(access_key, client.hashed_password):
        logger.error("AccessKey verification failed")
        return False
    return client

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_username(db: Session, client_id: str):
    return db.query(Client).filter(Client.client_id == client_id).first()

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None:
            logger.error("Username not found in token")
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise credentials_exception
    except jwt.InvalidTokenError:
        logger.error("Invalid token")
        raise credentials_exception
    client = get_user_by_username(db, client_id)
    if client is None:
        logger.error("Client not found for token")
        raise credentials_exception
    return client

@app.get("/", response_class=HTMLResponse)
async def get_client():
    with open("static/index.html", "r") as file:
        return file.read()

@app.post("/register/", response_model=UserResponse)
def register_user(client: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(client.access_key)
    db_user = Client(
        client_id=client.client_id,
        email=client.email,
        full_name=client.full_name,
        hashed_password=hashed_password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    client = authenticate_user(db, form_data.client_id, form_data.access_key)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect client_id or access_key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": client.client_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: Annotated[Client, Depends(get_current_user)]):
    return current_user

@app.get("/users/{client_id}", response_model=UserResponse)
def read_user_by_username(client_id: str, db: Session = Depends(get_db)):
    client = get_user_by_username(db, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.get("/users/", response_model=list[UserResponse])
def get_users(current_user: Annotated[Client, Depends(get_current_user)], db: Session = Depends(get_db)):
    users = db.query(Client).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    try:
        return [UserResponse.model_validate(client) for client in users]
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, current_user: Annotated[Client, Depends(get_current_user)], db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == user_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return client

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, current_user: Annotated[Client, Depends(get_current_user)], user_update: UserUpdate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == user_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    if user_update.email and user_update.email != client.email:
        existing_user = db.query(Client).filter(Client.email == user_update.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    if user_update.client_id:
        client.client_id = user_update.client_id
    if user_update.email:
        client.email = user_update.email
    if user_update.full_name:
        client.full_name = user_update.full_name
    if user_update.access_key:
        client.hashed_password = hash_password(user_update.access_key)
    if user_update.disabled is not None:
        client.disabled = user_update.disabled
    try:
        db.commit()
        db.refresh(client)
        return client
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.get("/test/")
def test_route():
    return {"message": "Test route is working"}

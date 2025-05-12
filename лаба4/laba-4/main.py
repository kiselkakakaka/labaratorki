from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://isp_r_kiselev:12345@77.91.86.135/isp_r_kiselev"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Client(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(100))
    disabled = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    client_id: str
    email: str
    full_name: str | None = None
    access_key: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    client_id: str | None = None

class UserUpdate(BaseModel):
    client_id: str | None = None
    email: str | None = None
    full_name: str | None = None
    access_key: str | None = None
    disabled: bool | None = None

class UserResponse(BaseModel):
    id: int
    client_id: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None
    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None:
            raise credentials_exception
        token_data = TokenData(client_id=client_id)
    except InvalidTokenError:
        raise credentials_exception
    client = get_user(user_name=token_data.client_id, db=db)
    if client is None:
        raise credentials_exception
    return client

async def get_current_active_user(current_user: Annotated[Client, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive client")
    return current_user

def get_user(user_name: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.client_id == user_name).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.get("/users/", response_model=list[UserResponse])
async def get_users(current_user: Annotated[Client, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    users = db.query(Client).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users

def hash_password(access_key: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(access_key.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(access_key):
    return pwd_context.hash(access_key)

def authenticate_user(db: Session, client_id: str, access_key: str):
    client = get_user(user_name=client_id, db=db)
    if not client:
        return False
    if not verify_password(access_key, client.hashed_password):
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

@app.get("/", response_class=HTMLResponse)
async def get_client():
    with open("static/index.html", "r") as file:
        return file.read()

@app.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, current_user: Annotated[Client, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    client = db.query(Client).filter(Client.id == user_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
    return client

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, current_user: Annotated[Client, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    client = db.query(Client).filter(Client.id == user_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    if user_update.client_id:
        client.client_id = user_update.client_id
    if user_update.email:
        client.email = user_update.email
    if user_update.full_name:
        client.full_name = user_update.full_name
    if user_update.access_key:
        client.hashed_password = get_password_hash(user_update.access_key)
    if user_update.disabled is not None:
        client.disabled = user_update.disabled

    try:
        db.commit()
        db.refresh(client)
        return client
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or Email already registered")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
async def read_users_me(current_user: Annotated[Client, Depends(get_current_active_user)]):
    return current_user

@app.post("/register/", response_model=UserResponse)
def register_user(client: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(client.access_key)
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
        raise HTTPException(status_code=400, detail="Username or Email already registered")

origins = [
"http://localhost.tiangolo.com",
"https://localhost.tiangolo.com",
"http://localhost",
"http://localhost:8080",
"http://allowed-origin.com",
]
app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), label="static")
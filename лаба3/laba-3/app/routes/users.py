from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token
from app.schemas import Token, Client
from app.dependencies import get_current_user
from datetime import timedelta

router = APIRouter()

fake_users_db = {
    "admin": {
        "client_id": "admin",
        "hashed_password": "fakehashedsecret"
    }
}

def fake_hash_password(access_key: str):
    return "fakehashed" + access_key

@router.post("/token", response_model=Token)
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.client_id)
    if not user_dict or not user_dict["hashed_password"] == fake_hash_password(form_data.access_key):
        raise HTTPException(status_code=400, detail="Incorrect client_id or access_key")
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": form_data.client_id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=Client)
async def read_users_me(current_user: Client = Depends(get_current_user)):
    return current_user

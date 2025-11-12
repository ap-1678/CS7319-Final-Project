from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict

app = FastAPI(title="user-service", version="0.1.0")

class UserIn(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str

DB: Dict[int, UserOut] = {}
_next_id = 1

@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(u: UserIn):
    global _next_id
    if any(x.email == u.email for x in DB.values()):
        raise HTTPException(status_code=409, detail="email already exists")
    user = UserOut(id=_next_id, email=u.email, username=u.username)
    DB[_next_id] = user
    _next_id += 1
    return user

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = DB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="not found")
    return user

from pydantic import BaseModel, EmailStr, conint
from datetime import datetime



         
class UserBase(BaseModel):
    email : EmailStr
    username : str


class UserCreate(UserBase):
    password : str

class User(BaseModel):
    id: int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenPayload(BaseModel):
    user_id : int


################################# POSTS ################################

class PostBase(BaseModel):
    title : str
    content: str
    published : bool  = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int   
    created_at : datetime
    owner: User

    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    Post: Post
    votes:int
    
    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id : int
    # user_id : int
    dir : int
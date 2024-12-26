from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    age: int

app = FastAPI()
users = []

@app.get("/users")
async def get_users() -> list:
    return users

@app.post("/user/{username}/{age}", response_model=User )
async def post_user(username: str, age: int) -> User:
    if not users:
        new_id = 1
    else:
        new_id = users[-1].id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", response_model=User )
async def update_user(user_id: int,
                      username: str = Path(min_length=5, max_length=20,
                                           description="Enter username", example='UrbanUser '),
                      age: int = Path(ge=18, le=120, description="Enter age", example=24)) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User  was not found')

@app.delete('/user/{user_id}', response_model=User )
async def delete_user(user_id: int) -> User:
    for index, user in enumerate(users):
        if user.id == user_id:
            return users.pop(index)  # Возвращаем удаленного пользователя
    raise HTTPException(status_code=404, detail='User  was not found')

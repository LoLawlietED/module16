from fastapi import FastAPI, HTTPException

app = FastAPI()

users = {"1": "Имя: Example, возраст: 18"}

@app.get('/users')
async def get_users():
    return users

@app.post("/users/{username}/{age}")
async def post_users(username: str, age: int):
    if age < 0:
        raise HTTPException(status_code=400, detail="Возраст не может быть отрицательным")
    
    user_id = str(int(max(users, key=int)) + 1)
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f"User  {user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: str, username: str, age: int) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if age < 0:
        raise HTTPException(status_code=400, detail="Возраст не может быть отрицательным")
    
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"The user {user_id} is updated"


@app.delete("/user/{user_id}")
async def delete_users(user_id: str) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    users.pop(user_id)
    return f"Message with {user_id} was deleted!"

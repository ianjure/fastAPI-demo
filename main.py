import json
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# User schema
class UserCreate(BaseModel):
    user_id: int
    username: str

# Function to save user as a new row to CSV file
def save_to_csv(user_id, username):
    df = pd.read_csv("db.csv")
    df.loc[len(df)] = [user_id, username]
    df.to_csv("db.csv", index=False)
    print("Saved!")

# Create user route
@app.post("/create_user/")
async def create_user(user_data: UserCreate):
    user_id = user_data.user_id
    username = user_data.username
    save_to_csv(user_id, username)
    return {
        "msg": "Data received!",
        "user_id": user_id,
        "username": username,
    }

# Get users route
@app.get("/")
def get_users():
    df = pd.read_csv("db.csv")
    json_df = df.to_json(orient="records")
    return json.loads(json_df)
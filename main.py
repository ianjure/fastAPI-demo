import os
import json
#import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# [SUPABASE] FETCHING DATA FROM THE DATABASE
def fetch_data(table):
    response = supabase.table(table).select('*').execute()
    if response.data:
        data = pd.DataFrame(response.data)
        return data

app = FastAPI()

# User schema
class UserCreate(BaseModel):
    user_id: int
    username: str

# Function to save user as a new row to CSV file
"""
def save_to_csv(user_id, username):
    df = pd.read_csv("db.csv")
    df.loc[len(df)] = [user_id, username]
    df.to_csv("db.csv", index=False)
    print("Saved!")
"""

# Create user route
@app.post("/create_user/")
async def create_user(user_data: UserCreate):
    user_id = user_data.user_id
    username = user_data.username
    data = {
        "user_id": id,
        "username": username
    }
    supabase.table("Test").insert(data).execute()
    return {
        "msg": "Data received!",
        "user_id": user_id,
        "username": username
    }

# Get users route
@app.get("/")
def get_users():
    df = fetch_data("Test")
    json_df = df.to_json(orient="records")
    return json.loads(json_df)

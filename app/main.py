from fastapi import FastAPI
from supabase import create_client, Client
from decouple import config

app = FastAPI()

url: str = config("SUPABASE_URL")
key: str = config("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.get("/")
async def root():
    return {"message": "Welcome to the Fish Stocking API, with the the fishy shit you need to know"}

@app.get("/ndow_stocking_records")
def ndow_all_records():
    all_records = supabase.table("ndow_fish_stocking").select('*').execute()
    return all_records
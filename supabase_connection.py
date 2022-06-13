from supabase import create_client, Client
from decouple import config
import pandas as pd

url: str = config("SUPABASE_URL")
key: str = config("SUPABASE_KEY")

supabase: Client = create_client(url, key)

df = pd.read_csv("data.csv", index_col=0)

ndow_table = supabase.table("ndow_fish_stocking").select("*").execute()

# if dataframe is empty build it up
try:  
  current_data = pd.DataFrame(ndow_table.data).drop("id", axis=1)

  if df.equals(current_data):
    print("WE GOOD")
  else:
    print("WE NOT GOOD")
    df = df.merge(current_data, on=["date", "water_name", "total_stocked", "species"], how='left', indicator=True).query('_merge == "left_only"')
    if len(df) > 0:
      for index, row in df.iterrows():
        configuration = {"date":row["date"], "water_name":row["water_name"], "total_stocked":row["total_stocked"], "species":row["species"]}
        data = supabase.table("ndow_fish_stocking").insert(configuration).execute()

except:
  current_data = pd.DataFrame(ndow_table.data)

  for index, row in df.iterrows():
      configuration = {"date":row["date"], "water_name":row["water_name"], "total_stocked":row["total_stocked"], "species":row["species"]}
      data = supabase.table("ndow_fish_stocking").insert(configuration).execute()

ndow_table = supabase.table("ndow_fish_stocking").select("*").execute()
print(ndow_table)
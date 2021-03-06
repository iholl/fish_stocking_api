import requests
import pandas as pd

data = {"event_id":[],"date":[], "water_name":[], "species": [], "total_stocked":[], "length":[], "annual_total_stocked":[]}

pages = ["1"]

url = "https://www.ndow.org/wp-json/wp/v2/event/?topic_category=322&per_page=1"

response = requests.get(url)
length_json = len(response.json())

# url = "https://www.ndow.org/wp-json/wp/v2/event/?topic_category=322&per_page={}&page={}".format(length_json, page)
# response = requests.get(url)

r1 = 0
r2 = len(response.json())

res = []
while(r1 < r2+1 ):
    res.append(r1)
    r1 += 1

for item in res:
  print(response.json()[item])
  excerpt = response.json()[item]["excerpt"]["rendered"].replace(": ", ":").split("Stocking")
  
  if excerpt[0].startswith("<p>Stocked"):
    data["event_id"].append(response.json()[item]["id"])
  
    data["date"].append(response.json()[item]["acf"]["date"]["start"])

    split = excerpt[0].replace("<p>","").split(" ")

    data["species"].append(split[1])
    
    for item in split: 
      if "Stocked:" in item:
        stocked = item.split(":")[1]
        data["total_stocked"].append(stocked.replace('"', "").replace(",", ""))
      elif "Length:" in item:
        length = item.split(":")[1]
        data["length"].append(length)
      elif "YTD:" in item:
        year_to_date = item.split(":")[1]
        data["annual_total_stocked"].append(year_to_date.replace('"', "").replace(",", ""))

df = pd.DataFrame.from_dict(data)
df.to_csv("data_api.csv")
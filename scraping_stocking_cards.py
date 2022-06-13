import requests
import pandas as pd
from bs4 import BeautifulSoup

data = {"water_name":[], "date":[], "species":[], "total_stocked":[], "annual_total_stocked":[]}

def get_page_data(parsed_soup):
  job_elements = parsed_soup.find_all("div", class_="database-card")

  for job_element in job_elements:
    title_element = job_element.find("h6", class_="database-card__title")
    data_element = job_element.find_all("dd")
    
    data["water_name"].append(title_element.text.strip())
    data["date"].append(data_element[2].text.strip())
    data["species"].append(data_element[1].text.strip())
    data["total_stocked"].append(data_element[0].text.strip())
    data["annual_total_stocked"].append(data_element[3].text.strip())

response = requests.get("https://www.ndow.org/get-outside/fishing/fishing-stocking-reports/database/?region=all&reports=stocking&show_all=true")
 
page = response.content
soup = BeautifulSoup(page, "html.parser")

get_page_data(soup)

page_list = []
pages = soup.find_all("a", class_="page-numbers")
for page in pages:
  try:
    number = int(page.text)
    page_list.append(number)    
  except ValueError:
    print("not an int")

max_page = max(page_list)
all_pages = list(range(1, max_page+1))

for page_number in all_pages:
  response = requests.get("https://www.ndow.org/get-outside/fishing/fishing-stocking-reports/database/page/{}/?region=all&reports=stocking&show_all=true".format(page_number))
 
  page = response.content
  soup = BeautifulSoup(page, "html.parser")

  get_page_data(soup)

df = pd.DataFrame.from_dict(data)
df.to_csv("data_card.csv")
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/Users/ianholl/Documents/chromedriver/chromedriver", options=options)
driver.get("https://www.ndow.org/calendar/#")

driver.find_element_by_xpath("// li[contains(text(),\'Fishing')]").click()

page_source = driver.page_source

data = {"date":[], "event":[]}

soup = BeautifulSoup(page_source, "html.parser")
job_elements = soup.find_all("div", class_="fc-daygrid-day-frame fc-scrollgrid-sync-inner")

date_list = []

for job_element in job_elements:
  date = job_element.find("a", class_="fc-daygrid-day-number")
  if date != None:
    date_list.append(date['aria-label'])
  events = job_element.find_all("div", class_="fc-daygrid-event-harness")
  for event in events: 
    title_element = event.find("div", {"class": "fc-event-title"})
    if len(title_element.attrs["class"]) == 1:
      data["event"].append(title_element.text.strip())
      data["date"].append(date_list[0])
  date_list = []
driver.close()

df = pd.DataFrame.from_dict(data)

split_df = df["event"].str.split("-", expand=True)
stripped = split_df.replace(r"^ +| +$", r"", regex=True)

water_name_df = stripped.drop(1, axis=1)
name_df = water_name_df.rename(columns={0:"water_name"})

count_species = stripped[1].str.split(" ", expand=True)
count_species_df = count_species.rename(columns={0:"total_stocked", 1:"species"})

water_count_species = pd.merge(name_df, count_species_df, left_index=True, right_index=True)

final_df = pd.merge(df["date"], water_count_species, left_index=True, right_index=True)
print(final_df)
final_df.to_csv("data.csv")
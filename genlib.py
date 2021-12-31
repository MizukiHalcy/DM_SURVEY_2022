import requests
import math
import re
from bs4 import BeautifulSoup
import pandas

from config import BASE_URL, CREATURES_NAME_XLSX_PATH, TRIBE_ID_CSV_PATH

tribe = "アーマード・ドラゴン"
df = pandas.read_csv(filepath_or_buffer=TRIBE_ID_CSV_PATH, encoding="shift_jis", engine="python")
data = df.query(f'name == "{tribe}"')
tribe_id = data.at[0, "id"]

def getCreatures(url): 
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    names = list(map(lambda x: re.sub(r'/.*', "", x.get_text()), soup.select(".ranktitle")))
    return names

creatures = []
url = f"{BASE_URL}?race[]={tribe_id}"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
total = int(re.search(r"\d+", soup.select_one("#resultboxes").get_text()).group())
offset = math.ceil(total / 100)
for x in range(offset):
    page = str(x + 1)
    url = url + f"&p={page}"
    creatures.extend(getCreatures(url))

uniqueCreatures = list(set(creatures))

result = pandas.DataFrame(uniqueCreatures)
result.to_excel(CREATURES_NAME_XLSX_PATH, sheet_name=tribe)
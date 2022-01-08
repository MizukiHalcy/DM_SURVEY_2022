import requests
import math
import re
from bs4 import BeautifulSoup
import pandas

from config import BASE_URL, CREATURES_NAME_XLSX_PATH, TRIBE_ID_CSV_PATH

tribe = "アーマード・ドラゴン"
df = pandas.read_csv(filepath_or_buffer=TRIBE_ID_CSV_PATH, encoding="shift_jis", engine="python")
data = df.query(f'name == "{tribe}"')
tribe_id = data.iat[0, 1]

def getCreatures(url): 
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    names = list(map(normalize, soup.select(".ranktitle")))
    return names

def normalize(token):
    text = token.get_text()
    raw1 = re.sub(r'／.*', "", text)
    raw2 = re.sub(r'/.*', "", raw1)
    raw3 = re.sub(r'[＜＞&<>・-]', " ", raw2)
    return raw3

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
with pandas.ExcelWriter(CREATURES_NAME_XLSX_PATH, mode="a") as writer:
    result.to_excel(writer, sheet_name=tribe)
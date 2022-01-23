import csv

results = []
with open('dostoevsky.csv', encoding="utf-8") as File:
    reader = csv.DictReader(File)
    for row in reader:
        results.append(row)

a = ""
for i in results:
    name = i["name"]
    url = i["url"]
    year = i["year"]
    country = i["country"]
    description = i["description"]
    wiki = i["wiki"]
    kinopoisk = i["kinopoisk"]
    id_kinopoisk = "".join([k for k in kinopoisk if k in "0123456789"])
    pic = i["pic"]
    
    a += (f"""
## {name}

<img src="{pic}" alt="drawing" width="225" align="right"/>

**Год:** {year}<br>
**Страна:** {country}

{description}<br>
<br><a href='{url}'><img src='https://github.com/MaksPV/Dostoevsky/raw/main/playbutt.png' border='0'></a><a href='{wiki}'><img src='https://github.com/MaksPV/Dostoevsky/raw/main/wikiread.png' border='0'></a><a href='{kinopoisk}'><img src='https://rating.kinopoisk.ru/{id_kinopoisk}.gif' border='0'></a><br clear="right"/>
""")

with open("README.md", "w", encoding="utf-8") as f:
    f.write(a)
    f.close()
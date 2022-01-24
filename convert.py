import csv
import time

import requests

results = []
with open('dostoevsky.csv', encoding="utf-8") as File:
    reader = csv.DictReader(File)
    for row in reader:
        results.append(row)

headers = {'X-API-KEY': 'b49a04fd-a84a-4a14-a02c-ca3dc3320b9f',
           'Content-Type': 'application/json'}

timer = 0
a = ""
rzdel = list()
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
    film_id = id_kinopoisk

    print(name)

    if i["original"] not in rzdel:
        rzdel.append(i["original"])
        a += f"# {i['original']}\n"

    if film_id:
        time.sleep(1 / 20)
        r = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}", headers=headers)
        js = r.json()
        time.sleep(1 / 20)
        r1 = requests.get(f"https://kinopoiskapiunofficial.tech/api/v1/staff/", params={"filmId": film_id},
                          headers=headers)
        js1 = r1.json()

        description = js["description"]
        film_length = js["filmLength"]
        if film_length is not None:
            timer += film_length
        else:
            film_length = "-"
        genres = [i["genre"] for i in js["genres"]]
        countries = [i["country"] for i in js["countries"]]
        year = js["year"]
        if pic == "https://s3.afisha.ru/mediastorage/ba/2e/6388c71dbba74e15919d824b2eba.jpg":
            pic = js["posterUrl"]

        staff = dict()
        for i in js1:
            if i["professionText"] not in staff:
                staff[i["professionText"]] = list()
            staff[i["professionText"]].append(i["nameRu"])

        staff_ = ""
        for k, i in list(staff.items())[:4]:
            staff_ += "**" + k + "**: " + ", ".join(i[:4]) + "<br>\n"

        if js["nameOriginal"] is None:
            res = f'## {js["nameRu"]}' + "\n\n"
        else:
            res = f'## {js["nameRu"]} / ориг. {js["nameOriginal"]}' + "\n\n"
        if pic:
            res += f'<img src="{pic}" border="3" alt="drawing" width="225" align="right"/>' + "\n\n"

        res += f"**Жанры:** {', '.join(genres)}<br>" + "\n"
        res += f"**Год:** {year}<br>" + "\n"
        res += f"**Страна:** {', '.join(countries)}<br>" + "\n"
        res += f"**Продолжительность:** {film_length} минут<br>" + "\n"

        g = {"Кинопоиск": js['ratingKinopoisk'],
             "IMDB": js['ratingImdb'],
             "Критики": js['ratingFilmCritics']}

        g_ = list()
        for k, i in g.items():
            if i is not None:
                g_.append(f"**{k}**: {i}")
        res += ", ".join(g_)
        res += "<br>\n\n"
        if description is not None:
            res += f"{description}<br><br>" + "\n"
        res += staff_ + "\n"
        res += f"<a href='{url}'><img src='https://github.com/MaksPV/Dostoevsky/raw/main/playbutt.png' border='0'></a>"
        if wiki:
            res += f"<a href='{wiki}'><img src='https://github.com/MaksPV/Dostoevsky/raw/main/wikiread.png' border='0'></a>"
        if id_kinopoisk:
            res += f"<a href='{kinopoisk}'><img src='https://rating.kinopoisk.ru/{id_kinopoisk}.gif' border='0'></a><br clear='right'/>"
        res += "\n\n"
    else:
        res = f"## {name}" + "\n\n"
        if pic:
            res += f'<img src="{pic}" border="3" alt="drawing" width="225" align="right"/>' + "\n\n"
        res += f"**Год:** {year}<br>" + "\n"
        res += f"**Страна:** {country}" + "\n\n"
        res += f"{description}<br>" + "\n"
        res += f"<br>"
        res += f"<a href='{url}'><img src='https://github.com/MaksPV/Dostoevsky/raw/main/playbutt.png' border='0'></a>"
        if wiki:
            res += f"<a href='{wiki}'><img src='https://github.com/MaksPV/Dostoevsky/raw/main/wikiread.png' border='0'></a>"
        if id_kinopoisk:
            res += f"<a href='{kinopoisk}'><img src='https://rating.kinopoisk.ru/{id_kinopoisk}.gif' border='0'></a><br clear='right'/>"
        res += "\n\n"

    a += res

res = ""
for i in rzdel:
    formated = i.lower().replace(" ", "-")
    res += f"- [{i}](#{formated})\n"

a = res + "\n" + a

with open("README.md", "w", encoding="utf-8") as f:
    f.write(a)
    f.close()
print(timer)
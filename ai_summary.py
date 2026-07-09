import json
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)


# Hírek betöltése
with open("news.json", "r", encoding="utf-8") as f:
    news = json.load(f)


# Kategóriánként csak a legfontosabb alapanyag
categories = {
    "Hungary": [],
    "AI": [],
    "Space": [],
    "Science": [],
    "World": [],
    "Politics": [],
    "Other Hungary": []
}


for item in news:
    cat = item.get("category", "")

    if cat in categories:
        categories[cat].append(item)


# Maximum hírek elküldése az AI-nak
selected_news = []

for cat, items in categories.items():
    selected_news.extend(items[:20])


news_text = ""

for item in selected_news:
    news_text += f"""
Cím: {item['title']}
Forrás: {item.get('source','')}
Kategória: {item.get('category','')}
Nyelv: {item.get('language','en')}
Link: {item['link']}

"""


prompt = f"""
Te egy prémium reggeli hírszerkesztő AI vagy.

Készíts egy Morning Briefing-et.

A cél:
Egy elfoglalt ember 5 perc alatt átlássa a nap legfontosabb híreit.


FONTOS SZABÁLYOK:

- Ne a forrás alapján dönts a kategóriáról.
- Egy Telex/HVG hír is lehet technológiai vagy világpolitikai.
- Ne rakj külföldi hírt a Magyarország kategóriába.
- Ugyanazt a hírt csak egyszer használd.
- Ne válassz clickbait vagy jelentéktelen híreket.


KATEGÓRIÁK ÉS DARABSZÁM:

🇭🇺 Magyarország
- 2 általános magyar hír

🏛️ Magyar politika
- 2 politikai magyar hír

🤖 AI & Technológia
- 2 hír

🚀 Űripar
- 2 hír

🔬 Tudomány
- 3 hír

🌍 Világpolitika
- 2 hír


PONTOZÁS:

Minden hír kiválasztásánál gondold végig:

- globális hatás
- hosszútávú jelentőség
- mennyire friss
- mennyire érdekes az olvasónak


FORMÁTUM:

Ne használj # jeleket.

Pontosan így:

🌅 Morning Briefing


🇭🇺 Magyarország


📰 Eredeti cím


📌 Röviden:
2-3 mondat magyarul


🎯 Miért fontos?
1 értelmes mondat, ami elmagyarázza a jelentőségét


🔗 Tovább:
link


NYELV:

- A cím mindig maradjon eredeti nyelven.
- Magyar hír → magyar összefoglaló.
- Angol hír → angol összefoglaló.


A végén:

📌 Mai trendek

3-5 pont:
- milyen nagy folyamatok látszanak
- ne csak ismételd a híreket


HÍREK:

{news_text}

"""


response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.3
)


summary = response.choices[0].message.content


with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)


print(summary)
print("\nMentve: summary.txt")

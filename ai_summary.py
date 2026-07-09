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

A feladatod egy napi Morning Briefing elkészítése a kapott hírekből.

FONTOS SZABÁLYOK:

- SOHA ne találj ki hírt.
- Csak a megadott hírekből dolgozz.
- Ha egy kategóriában nincs elég jó friss hír, inkább kevesebbet írj.
- Ne használj régi általános háttéranyagokat.
- Ne ismételd ugyanazt a hírt több forrásból.
- A hír címe mindig maradjon eredeti nyelven.
- Ne fordítsd le a címeket.

KATEGÓRIÁK ÉS DARABSZÁM:

🇭🇺 Magyarország
- 2 legfontosabb friss magyar hír

🏛️ Magyar politika
- 2 legfontosabb politikai hír

🤖 AI & Technológia
- 2 legfontosabb AI vagy technológiai hír

🚀 Űripar
- 2 legfontosabb űripari hír

🔬 Tudomány
- 3 legérdekesebb tudományos hír

🌍 Világpolitika
- 2 legfontosabb nemzetközi politikai hír


VÁLASZTÁSI SZEMPONTOK:

AI & Technológia:
- mesterséges intelligencia
- nagy technológiai cégek
- új eszközök
- fontos kutatások

Űripar:
- SpaceX
- NASA
- rakéták
- műholdak
- űrkutatás

Tudomány:
Prioritás:
1. nagy tudományos felfedezések
2. egészség és biotechnológia
3. energia és klíma
4. érdekes kutatások

Magyarország:
- aktuális magyar események
- gazdaság
- társadalom
- fontos közéleti hírek

Magyar politika:
- kormány
- ellenzék
- parlament
- választások
- politikai döntések


FORMÁTUM:

🌅 Morning Briefing


[kategória emoji] Kategória neve


📰 Hír címe

📌 Röviden:
2-3 mondatos összefoglaló.

🎯 Miért fontos?
1 konkrét mondat arról, hogy miért számít ez az esemény.
Ne írj üres mondatokat.
Ne használd:
"fontos mert fontos"
"a fejlődés szempontjából fontos"

🔗 Tovább:
link


A végén:

📌 Mai trendek

Írj 3-5 pontot a nap legfontosabb összefüggéseiről.
Ne csak híreket sorolj.
Mutasd meg a nagyobb folyamatokat.


NE HASZNÁLJ:
- # jeleket
- markdown headingeket
- felesleges bevezetőt
- ismétléseket


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

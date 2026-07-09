import json
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)


# -----------------------------
# Hírek betöltése
# -----------------------------

with open("news.json", "r", encoding="utf-8") as f:
    news = json.load(f)


# maximum ennyi hírt küldünk az AI-nak
news_text = ""

for item in news[:200]:

    news_text += f"""
Cím: {item.get('title', '')}
Forrás: {item.get('source', '')}
Kategória: {item.get('category', '')}
Nyelv: {item.get('language', '')}
Link: {item.get('link', '')}

"""


# -----------------------------
# AI prompt
# -----------------------------

prompt = f"""
Te egy prémium reggeli hírszerkesztő AI vagy.

Készíts egy Morning Briefing-et az alábbi hírekből.

FONTOS:
Ne a 10 legjobb hírt válaszd összesen.
Minden kategóriából kötelező válogatni.


KATEGÓRIÁK:

🇭🇺 Magyarország

🏛️ Magyar politika:
- pontosan 2 hír

📰 Egyéb magyar hírek:
- pontosan 2 hír


🤖 AI & Technológia:
- pontosan 2 hír


🚀 Űripar:
- pontosan 2 hír


🔬 Tudomány:
- pontosan 3 hír


🌍 Világpolitika:
- pontosan 2 hír


SZABÁLYOK:

- Ugyanaz a hír csak egyszer szerepelhet.
- Ha több oldal ír ugyanarról, csak a legjobb forrást használd.
- Ne válassz reklámokat, termékakciókat vagy jelentéktelen híreket.
- A cím maradjon az eredeti nyelven.
- Ne fordítsd le a címet.

NYELV:

- Magyar hír esetén magyarul írj.
- Angol hír esetén angolul írj.


FORMÁTUM:


🌅 Morning Briefing


🇭🇺 Magyarország


🏛️ Magyar politika


📰 Cím


📌 Röviden:
2-3 mondat


🎯 Miért fontos?
1 mondat


🔗 Tovább:
link



📰 Egyéb magyar hírek

(ugyanilyen formátum)



🤖 AI & Technológia


📰 Cím

📌 Röviden:
2-3 mondat

🎯 Miért fontos?
1 mondat

🔗 Tovább:
link



🚀 Űripar


(ugyanilyen formátum)



🔬 Tudomány


(ugyanilyen formátum)



🌍 Világpolitika


(ugyanilyen formátum)



A végén:


📌 Mai trendek


3-5 pontban írd le a legfontosabb hosszabb távú folyamatokat.


HÍREK:

{news_text}

"""


# -----------------------------
# AI hívás
# -----------------------------

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


# -----------------------------
# Mentés
# -----------------------------

with open(
    "summary.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(summary)


print(summary)
print("\nMentve: summary.txt")

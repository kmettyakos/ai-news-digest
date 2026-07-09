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


# -----------------------------
# Kategóriánként előszűrés
# -----------------------------

categories = {}

for item in news:

    category = item.get("category", "OTHER")

    if category not in categories:
        categories[category] = []

    # kategóriánként maximum 15 jelölt
    if len(categories[category]) < 15:
        categories[category].append(item)



news_text = ""

for category, items in categories.items():

    news_text += f"\n\n===== {category} =====\n"

    for item in items:

        news_text += f"""
Cím: {item.get('title','')}
Forrás: {item.get('source','')}
Nyelv: {item.get('language','')}
Link: {item.get('link','')}

"""


# -----------------------------
# Prompt
# -----------------------------

prompt = f"""
Te egy prémium reggeli hírszerkesztő AI vagy.

A feladatod egy Morning Briefing készítése.

Válassz híreket ezekbe a kategóriákba:


🇭🇺 Magyarország

🏛️ Magyar politika:
2 hír


📰 Egyéb magyar hírek:
2 hír


🤖 AI & Technológia:
2 hír


🚀 Űripar:
2 hír


🔬 Tudomány:
3 hír


🌍 Világpolitika:
2 hír


SZABÁLYOK:

- Egy hír csak egyszer szerepelhet.
- Ha több forrás ugyanarról ír, csak egyet használj.
- Ne használj reklámot vagy termékakciót.
- A cím maradjon eredeti nyelven.
- Magyar hírt magyarul foglalj össze.
- Angol hírt angolul foglalj össze.


FORMÁTUM:


🌅 Morning Briefing


(kategóriák emoji címmel)


📰 Cím


📌 Röviden:
2-3 mondat


🎯 Miért fontos?
1 mondat


🔗 Tovább:
link



A végén:


📌 Mai trendek

3-5 pont a legfontosabb folyamatokról.


HÍREK:

{news_text}

"""


# -----------------------------
# AI
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

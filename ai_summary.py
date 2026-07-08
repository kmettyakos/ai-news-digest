import json
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)


with open("news.json", "r", encoding="utf-8") as f:
    news = json.load(f)


news_text = ""

for item in news[:60]:
    news_text += f"""
Cím: {item.get('title', '')}
Forrás: {item.get('source', '')}
Nyelv: {item.get('language', '')}
Link: {item.get('link', '')}

"""


prompt = f"""
Te egy személyes reggeli hírszerkesztő AI vagy.

Készíts egy 5 perc alatt elolvasható Morning Briefing-et.

SZABÁLYOK:

- Válaszd ki a 10 legfontosabb hírt.
- Szűrd ki az ismétlődéseket.
- Ne használj kattintásvadász híreket.
- Fókusz:
  - mesterséges intelligencia
  - technológia
  - tudomány
  - űripar
  - gazdaság
  - fontos világpolitika

NYELVI SZABÁLY:

- Magyar források esetén magyarul írj.
- Angol források esetén angolul írj.
- Ne fordítsd át a híreket más nyelvre.

FORMÁTUM:

# 🌅 Morning Briefing

## Kategória

### Hír címe

Mi történt:
(1-2 mondat)

Miért fontos:
(1 mondat)

Forrás:
(link)


A végén:

# 📌 Mai trendek

3-5 pontban írd le a legfontosabb folyamatokat.


Hírek:

{news_text}
"""


response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a professional news editor."
        },
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

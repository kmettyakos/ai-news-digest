import json
import os
import google.generativeai as genai


genai.configure(
    api_key=os.environ["GEMINI_API_KEY"]
)


model = genai.GenerativeModel("gemini-2.0-flash")


with open("news.json", "r", encoding="utf-8") as f:
    news = json.load(f)


# Csak a legfrissebb 60 hírt küldjük az AI-nak
news_text = ""

for item in news[:60]:
    news_text += f"""
Cím: {item['title']}
Forrás: {item['source']}
Nyelv: {item['language']}
Link: {item['link']}

"""


prompt = f"""
Te egy személyes reggeli hírszerkesztő AI vagy.

Készíts egy 5 perc alatt elolvasható Morning Briefing-et.

SZABÁLYOK:

- Válaszd ki a 10 legfontosabb hírt.
- Szűrd ki az ismétlődő híreket.
- Ne használj kattintásvadász híreket.
- Legyen fókusz:
  * mesterséges intelligencia
  * technológia
  * tudomány
  * űripar
  * gazdaság
  * fontos világpolitika


NYELVI SZABÁLY:

- Ha a "Nyelv" mező hu:
  → magyarul írj.

- Ha a "Nyelv" mező en:
  → angolul írj.

- Ne fordítsd át más nyelvre.


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


response = model.generate_content(prompt)


with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(response.text)


print(response.text)
print("\nMentve: summary.txt")

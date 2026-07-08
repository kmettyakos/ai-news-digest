import json
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)


with open("news.json", "r", encoding="utf-8") as f:
    news = json.load(f)


news_text = ""

for item in news[:40]:
    news_text += f"""
Cím: {item['title']}
Forrás: {item.get('source', '')}
Nyelv: {item.get('language', 'en')}
Link: {item['link']}

"""


prompt = f"""
Te egy személyes reggeli hírszerkesztő AI vagy.

Készíts egy Morning Briefing összefoglalót.

SZABÁLYOK:

- Válaszd ki a 10 legfontosabb hírt.
- Szűrd ki az ismétlődő híreket.
- Ne legyen clickbait.
- Fókusz:
  - mesterséges intelligencia
  - technológia
  - tudomány
  - űripar
  - gazdaság
  - világpolitika


NYELV:

Ha a hír nyelve "hu":
→ magyar összefoglaló

Ha "en":
→ angol összefoglaló


FORMÁTUM:

# 🌅 Morning Briefing


## Hír címe

Mi történt:
2 mondat

Miért fontos:
1 mondat

Forrás:
link


A végén:

# 📌 Mai trendek

3-5 pont.


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
    ]
)


summary = response.choices[0].message.content


with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)


print(summary)
print("\nMentve: summary.txt")

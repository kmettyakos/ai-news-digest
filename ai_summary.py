import json
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)


with open("news.json", "r", encoding="utf-8") as f:
    news = json.load(f)


# maximum 120 hír megy az AI-nak, hogy ne legyen túl nagy request
news = news[:120]


news_text = ""

for item in news:
    news_text += f"""
Cím: {item['title']}
Forrás: {item.get('source', '')}
Kategória: {item.get('category', '')}
Nyelv: {item.get('language', '')}
Link: {item['link']}

"""


prompt = f"""
Te egy prémium reggeli hírszerkesztő AI vagy.

Készíts egy Morning Briefing hírszemlét.

A híreket kategóriák szerint rendezd.

KATEGÓRIÁK:

🇭🇺 Magyarország
- 2 legfontosabb magyar hír

🏛️ Magyar politika
- 2 legfontosabb politikai hír

🤖 AI & Technológia
- 2 legfontosabb hír

🚀 Űripar
- 2 legfontosabb hír

🔬 Tudomány
- 3 legfontosabb hír

🌍 Világpolitika
- 2 legfontosabb hír


SZABÁLYOK:

- Egy hír csak egyszer szerepelhet.
- Ha ugyanaz a hír több forrásból van, csak a legjobb forrást használd.
- Ne találj ki híreket.
- Ha nincs elég releváns hír egy kategóriában, írd:
"Nincs elég releváns hír."
- A cím mindig maradjon az eredeti nyelven.
- A forrás linkje mindig maradjon meg.
- Ne használj Markdown fejléc jeleket (#).
- Csak emoji kategóriacímek legyenek.


FORMÁTUM:


🌅 Morning Briefing


🇭🇺 Magyarország


📰 Eredeti cím

📌 Röviden:
2-3 természetes magyar mondat.

🎯 Miért fontos?
1 konkrét mondat arról, hogy miért számít ez a hír.


🔗 Tovább:
link


A végén:


📌 Mai trendek


- 5 rövid pont a mai nap legfontosabb összefüggő trendjeiről.
- Ne általánosságokat írj.
- Kapcsolódjon konkrétan a mai hírekhez.


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

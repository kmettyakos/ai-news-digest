import json
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)


with open("news.json", "r", encoding="utf-8") as f:
    news = json.load(f)


# Maximum 120 hír küldése, hogy ne lépjük túl a token limitet
news_text = ""

for item in news[:120]:
    news_text += f"""
Cím: {item.get('title', '')}
Forrás: {item.get('source', '')}
Kategória: {item.get('category', '')}
Nyelv: {item.get('language', '')}
Link: {item.get('link', '')}

"""


prompt = f"""
Te egy prémium reggeli hírszerkesztő AI vagy.

Készíts egy napi Morning Briefing összefoglalót a kapott hírekből.

FONTOS SZABÁLYOK:

- Csak a megadott hírekből dolgozz.
- SOHA ne találj ki hírt.
- Ha nincs megfelelő hír egy kategóriában, inkább hagyd üresen vagy válassz kevesebbet.
- Ne használj régi általános háttéranyagokat.
- Ne használj ugyanazt a hírt több kategóriában.
- Ugyanazt az eseményt ne írd le több forrásból.
- A hír címe mindig maradjon eredeti nyelven.
- Ne fordítsd le a címeket.


A híreket rangsorold:

+3 pont: világszinten jelentős esemény
+3 pont: sok embert érint
+2 pont: nagy vállalat, ország vagy szervezet érintett
+2 pont: új technológia vagy tudományos áttörés
+1 pont: Magyarországhoz kapcsolódik

A magasabb pontszámú híreket válaszd.


KATEGÓRIÁK:


🇭🇺 Magyarország
2 legfontosabb friss magyar hír

🏛️ Magyar politika
2 legfontosabb magyar politikai hír

🤖 AI & Technológia
2 legfontosabb AI vagy technológiai hír

🚀 Űripar
2 legfontosabb űripari hír

🔬 Tudomány
3 legérdekesebb tudományos hír

Prioritás:
1. egészség
2. biotechnológia
3. energia
4. klíma
5. nagy tudományos felfedezések

Nagyon speciális kutatást csak akkor válassz, ha nincs érdekesebb.


🌍 Világpolitika
2 legfontosabb nemzetközi politikai hír



FORMÁTUM:


🌅 Morning Briefing


🇭🇺 Magyarország


📰 Eredeti cím

📌 Röviden:
2-3 mondatos összefoglaló.

🎯 Miért fontos?
1 konkrét mondat.
Magyarázd el a valódi jelentőségét.

Kerüld:
- "fontos mert fontos"
- "a fejlődés szempontjából fontos"
- általános üres mondatokat.


🔗 Tovább:
eredeti link



Minden kategóriát ugyanebben a formában írj.


A végén:


📌 Mai trendek

Írj 3-5 pontot a nap legfontosabb nagyobb folyamatairól.
Ne csak híreket ismételj.


TILOS:

- # jelek használata
- markdown headingek
- kitalált információ
- hiányzó linkek
- ismétlődő hírek


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

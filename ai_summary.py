import json
import os
from datetime import datetime
from openai import OpenAI


# ======================
# BEÁLLÍTÁSOK
# ======================

MODEL = "gpt-5-mini"
MAX_NEWS = 30


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# ======================
# NEWS BETÖLTÉS
# ======================

with open(
    "news.json",
    "r",
    encoding="utf-8"
) as f:

    news = json.load(f)


# csak legjobb hírek
news = news[:MAX_NEWS]


results = []


# ======================
# AI FELDOLGOZÁS
# ======================

for index, item in enumerate(news, start=1):

    title = item.get("title", "")

    if not title:
        continue


    print(
        f"[{index}/{len(news)}] {title}"
    )


    prompt = f"""
You are a professional news editor.

Analyze this article title.

Title:
{title}

Category:
{item.get("category")}

Source:
{item.get("source")}


Write a Hungarian news explanation.

Return ONLY valid JSON.

Format:

{{
"summary": "",
"why_it_matters": "",
"background": ""
}}


Rules:

summary:
- 2-3 sentences
- explain what happened
- factual only

why_it_matters:
- explain why this topic is important
- mention possible impact

background:
- provide short context
- explain things a normal reader needs to know

Do not invent facts.
If information is missing, say that the details are limited.
"""


    try:

        response = client.responses.create(

            model=MODEL,

            input=prompt,

            temperature=0.2
        )


        text = response.output_text.strip()


        # JSON tisztítás
        if text.startswith("```"):

            text = (
                text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )


        data = json.loads(text)


        item["summary"] = data.get(
            "summary",
            ""
        )

        item["why_it_matters"] = data.get(
            "why_it_matters",
            ""
        )

        item["background"] = data.get(
            "background",
            ""
        )


        item["processed_at"] = (
            datetime.now()
            .isoformat()
        )


        results.append(item)



        # mentés minden siker után
        with open(
            "daily_news.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                results,
                f,
                ensure_ascii=False,
                indent=2
            )


    except json.JSONDecodeError:

        print(
            "JSON hiba ennél:",
            title
        )

        continue


    except Exception as e:

        print(
            "AI hiba:",
            e
        )

        continue



# ======================
# VÉGE
# ======================

print()
print(
    "Kész!",
    len(results),
    "hír feldolgozva"
)

print(
    "Mentve: daily_news.json"
)

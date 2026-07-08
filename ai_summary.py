import json
import os
import google.generativeai as genai


genai.configure(
    api_key=os.environ["GEMINI_API_KEY"]
)


model = genai.GenerativeModel("gemini-2.0-flash")


with open("news.json", encoding="utf-8") as f:
    news = json.load(f)


text = "\n\n".join(
    [
        f"{n['title']}\n{n['link']}"
        for n in news[:50]
    ]
)


prompt = f"""
Te egy személyes reggeli hírszerkesztő vagy.

A következő hírekből készíts egy rövid napi összefoglalót.

Szabályok:
- csak a legfontosabb 10 hírt válaszd ki
- szűrd ki az ismétlődéseket
- legyenek kategóriák:
  Tech
  Tudomány
  Gazdaság
  Világ
- minden hírhez írj:
  1 mondatban mi történt
  1 mondatban miért fontos


Hírek:

{text}
"""


response = model.generate_content(prompt)


with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(response.text)


print(response.text)

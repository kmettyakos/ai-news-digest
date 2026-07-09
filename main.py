import feedparser
import json
import re

from datetime import datetime, timedelta
from urllib.parse import urlparse


# ==========================
# BEÁLLÍTÁSOK
# ==========================

DAYS_BACK = 14
MAX_PER_SOURCE = 10


# ==========================
# RSS FORRÁSOK
# ==========================

with open("sources.txt", "r", encoding="utf-8") as file:
    sources = [
        line.strip()
        for line in file.readlines()
        if line.strip() and not line.startswith("#")
    ]


news = []

date_limit = datetime.now() - timedelta(days=DAYS_BACK)



# ==========================
# KATEGÓRIA FELISMERÉS
# ==========================

def detect_category(title, summary, source):

    text = (title + " " + summary).lower()


    # AI
    if any(x in text for x in [
        "artificial intelligence",
        " ai ",
        "chatgpt",
        "openai",
        "anthropic",
        "llm",
        "machine learning",
        "deep learning",
        "neural network"
    ]):
        return "AI"


    # Space
    if any(x in text for x in [
        "nasa",
        "spacex",
        "starship",
        "rocket launch",
        "satellite",
        "spacecraft",
        "moon mission",
        "mars mission",
        "orbital"
    ]):
        return "Space"


    # Science
    if any(x in text for x in [
        "research",
        "study",
        "nature",
        "science",
        "biology",
        "medicine",
        "physics",
        "quantum"
    ]):
        return "Science"


    # Technology
    if any(x in text for x in [
        "google",
        "apple",
        "microsoft",
        "android",
        "iphone",
        "linux",
        "software",
        "cybersecurity",
        "chip",
        "processor",
        "rust",
        "typescript"
    ]):
        return "Technology"


    # Magyar
    if any(x in source for x in [
        "telex.hu",
        "hvg.hu",
        "24.hu",
        "444.hu",
        "index.hu",
        "mandiner.hu",
        "portfolio.hu"
    ]):
        return "Hungary"


    # Politika
    if any(x in text for x in [
        "government",
        "president",
        "prime minister",
        "election",
        "parliament",
        "minister",
        "war",
        "nato",
        "sanction",
        "military"
    ]):
        return "World"


    return "Other"



# ==========================
# SCORE
# ==========================

def calculate_score(category, source, date):

    score = 0


    trusted = [
        "nature.com",
        "science.org",
        "technologyreview.com",
        "theverge.com",
        "arstechnica.com",
        "spacenews.com",
        "bbc.com",
        "bbc.co.uk"
    ]


    if source in trusted:
        score += 3


    if category in [
        "AI",
        "Space",
        "Science",
        "Technology"
    ]:
        score += 3


    if date:
        if date > datetime.now()-timedelta(days=2):
            score +=2


    return score



# ==========================
# RSS FELDOLGOZÁS
# ==========================

for url in sources:

    print("Olvasom:", url)


    try:

        feed = feedparser.parse(url)


        for entry in feed.entries[:30]:


            title = entry.get("title","")
            link = entry.get("link","")
            summary = entry.get("summary","")


            # tisztítás
            link = re.sub(r"\[|\]|\(|\)", "", link)


            published = entry.get("published_parsed")


            article_date = None


            if published:

                article_date = datetime(*published[:6])


                if article_date < date_limit:
                    continue



            source = urlparse(link).netloc.replace(
                "www.",
                ""
            )


            category = detect_category(
                title,
                summary,
                source
            )


            score = calculate_score(
                category,
                source,
                article_date
            )


            language = "hu" if category=="Hungary" else "en"


            news.append({

                "title":title,

                "link":link,

                "source":source,

                "category":category,

                "language":language,

                "score":score,

                "date":
                    article_date.isoformat()
                    if article_date
                    else None

            })


    except Exception as e:

        print("Hiba:",e)



# ==========================
# DUPLIKÁCIÓ
# ==========================

unique={}


for item in news:

    key=item["title"].lower()

    if key not in unique:
        unique[key]=item


news=list(unique.values())



# ==========================
# FORRÁS LIMIT
# ==========================

filtered=[]

counter={}


for item in sorted(
    news,
    key=lambda x:x["score"],
    reverse=True
):

    source=item["source"]

    if counter.get(source,0)>=MAX_PER_SOURCE:
        continue


    filtered.append(item)

    counter[source]=counter.get(source,0)+1



news=filtered



# ==========================
# RENDEZÉS
# ==========================

news.sort(
    key=lambda x:x["score"],
    reverse=True
)



# ==========================
# MENTÉS
# ==========================

with open(
    "news.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        news,
        f,
        ensure_ascii=False,
        indent=2
    )


print()
print("Kész!")
print("Hírek:",len(news))

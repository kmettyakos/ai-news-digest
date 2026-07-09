import feedparser
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse


# RSS források betöltése

with open("sources.txt", "r", encoding="utf-8") as file:
    sources = [
        line.strip()
        for line in file.readlines()
        if line.strip() and not line.startswith("#")
    ]


all_news = []

# csak az elmúlt 14 nap hírei
date_limit = datetime.now() - timedelta(days=14)


def detect_category(title, summary, source):
    text = (title + " " + summary).lower()

    # magyar politika
    if any(x in text for x in [
        "orbán", "kormány", "parlament", "választás",
        "miniszter", "fidesz", "tisza", "ellenzék",
        "politika"
    ]):
        return "Politics"

    # magyar hírek
    if any(x in source for x in [
        "telex.hu",
        "hvg.hu",
        "24.hu",
        "444.hu",
        "index.hu",
        "mandiner.hu",
        "portfolio.hu",
        "vg.hu"
    ]):
        return "Hungary"


    # AI
    if any(x in text for x in [
        "ai",
        "artificial intelligence",
        "chatgpt",
        "openai",
        "anthropic",
        "google ai",
        "machine learning",
        "llm",
        "robot"
    ]):
        return "AI"


    # űripar
    if any(x in text for x in [
        "nasa",
        "spacex",
        "rocket",
        "satellite",
        "moon",
        "mars",
        "orbit",
        "space"
    ]):
        return "Space"


    # tudomány
    if any(x in text for x in [
        "research",
        "study",
        "science",
        "nature",
        "physics",
        "biology",
        "medicine",
        "quantum"
    ]):
        return "Science"


    # világpolitika
    if any(x in text for x in [
        "war",
        "president",
        "china",
        "russia",
        "iran",
        "usa",
        "europe",
        "government"
    ]):
        return "World"


    return "Other Hungary"



for url in sources:

    print("\nOlvasom:", url)

    try:
        feed = feedparser.parse(url)

        for entry in feed.entries[:30]:

            title = entry.get("title", "")
            link = entry.get("link", "")

            summary = entry.get("summary", "")

            # dátum ellenőrzés

            published = entry.get("published_parsed")

            if published:
                article_date = datetime(*published[:6])

                if article_date < date_limit:
                    continue


            source = urlparse(link).netloc.replace("www.", "")

            category = detect_category(
                title,
                summary,
                source
            )


            language = "hu" if any(x in source for x in [
                "telex",
                "hvg",
                "24.hu",
                "444",
                "index",
                "mandiner",
                "portfolio",
                "vg"
            ]) else "en"


            all_news.append({
                "title": title,
                "link": link,
                "source": source,
                "category": category,
                "language": language
            })


    except Exception as e:
        print("Hiba:", e)



# duplikátumok törlése

unique = {}

for item in all_news:
    key = item["title"].lower()

    if key not in unique:
        unique[key] = item


all_news = list(unique.values())



# ne legyen egy forrásból túl sok

filtered = []

source_count = {}

for item in all_news:

    source = item["source"]

    if source_count.get(source, 0) >= 15:
        continue

    filtered.append(item)

    source_count[source] = source_count.get(source, 0) + 1



all_news = filtered



with open("news.json", "w", encoding="utf-8") as f:
    json.dump(
        all_news,
        f,
        ensure_ascii=False,
        indent=2
    )


print("\nMentve:", len(all_news), "hír")

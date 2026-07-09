import feedparser
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse


with open("sources.txt", "r", encoding="utf-8") as file:
    sources = [
        line.strip()
        for line in file.readlines()
        if line.strip() and not line.startswith("#")
    ]


news = []

date_limit = datetime.now() - timedelta(days=14)


HUNGARIAN_SOURCES = [
    "telex.hu",
    "hvg.hu",
    "24.hu",
    "444.hu",
    "index.hu",
    "mandiner.hu",
    "portfolio.hu",
    "vg.hu"
]


def detect_category(title, summary, source):

    text = (title + " " + summary).lower()


    # magyar politika
    if any(x in text for x in [
        "orbán",
        "fidesz",
        "tisza",
        "parlament",
        "miniszter",
        "kormány",
        "választás",
        "ellenzék",
        "országgyűlés"
    ]):
        return "Politics"


    # magyar hírek
    if any(x in source for x in HUNGARIAN_SOURCES):
        return "Hungary"


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
        "robot"
    ]):
        return "AI"


    # űripar
    if any(x in text for x in [
        "nasa",
        "spacex",
        "rocket",
        "satellite",
        "orbit",
        "moon",
        "mars",
        "space"
    ]):
        return "Space"


    # tudomány
    if any(x in text for x in [
        "nature",
        "science",
        "research",
        "study",
        "physics",
        "biology",
        "medicine",
        "quantum"
    ]):
        return "Science"


    # világpolitika
    if any(x in text for x in [
        "war",
        "china",
        "russia",
        "iran",
        "ukraine",
        "president",
        "nato",
        "europe",
        "government"
    ]):
        return "World"


    return "Other"



def calculate_score(title, summary, source):

    text = (title + " " + summary).lower()

    score = 0


    important_words = [
        "breaking",
        "major",
        "first",
        "new",
        "launch",
        "discovery",
        "research",
        "openai",
        "nasa",
        "spacex",
        "google",
        "microsoft"
    ]

    for word in important_words:
        if word in text:
            score += 2


    if source in HUNGARIAN_SOURCES:
        score += 2


    if len(title) < 20:
        score -= 2


    return score



for url in sources:

    print("\nOlvasom:", url)

    try:

        feed = feedparser.parse(url)


        for entry in feed.entries[:40]:

            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")


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


            language = "hu" if source in HUNGARIAN_SOURCES else "en"



            news.append({

                "title": title,

                "link": link,

                "source": source,

                "category": category,

                "language": language,

                "score": calculate_score(
                    title,
                    summary,
                    source
                )

            })


    except Exception as e:
        print("Hiba:", e)




# duplikáció törlés

unique = {}

for item in news:

    key = item["title"].lower()

    if key not in unique:
        unique[key] = item


news = list(unique.values())



# pontszám alapján rendezés

news.sort(
    key=lambda x: x["score"],
    reverse=True
)



# forrás limit

final = []

source_count = {}


for item in news:

    source = item["source"]

    if source_count.get(source,0) >= 5:
        continue


    final.append(item)

    source_count[source] = source_count.get(source,0)+1



with open(
    "news.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        final,
        f,
        ensure_ascii=False,
        indent=2
    )


print(
    "\nMentve:",
    len(final),
    "hír"
)

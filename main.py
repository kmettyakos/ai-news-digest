import feedparser
import json
import re


def detect_language(category, title):
    """
    Egyszerű nyelvfelismerés.
    Magyar forrásokat automatikusan hu-nak vesz.
    """

    if category == "HUNGARY":
        return "hu"

    # gyakori magyar karakterek
    hungarian_chars = "áéíóöőúüűÁÉÍÓÖŐÚÜŰ"

    if any(char in title for char in hungarian_chars):
        return "hu"

    return "en"


def get_source_name(url):
    """
    Forrásnév kinyerése URL-ből
    """

    clean = url.replace("https://", "").replace("http://", "")
    domain = clean.split("/")[0]

    return domain.replace("www.", "")


# -----------------------------
# RSS források beolvasása
# -----------------------------

sources = []

current_category = "Other"

with open("sources.txt", "r", encoding="utf-8") as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        # kategória sor
        if line.startswith("[") and line.endswith("]"):
            current_category = line[1:-1]
            continue

        # komment
        if line.startswith("#"):
            continue

        sources.append({
            "url": line,
            "category": current_category
        })


# -----------------------------
# Hírek gyűjtése
# -----------------------------

all_news = []

seen_links = set()


for source in sources:

    url = source["url"]
    category = source["category"]

    print("\nOlvasom:", url)

    try:

        feed = feedparser.parse(url)

        source_name = get_source_name(url)


        for entry in feed.entries[:10]:

            title = entry.get(
                "title",
                "Nincs cím"
            )

            link = entry.get(
                "link",
                ""
            )


            # duplikáció kiszűrés
            if link in seen_links:
                continue

            seen_links.add(link)


            language = detect_language(
                category,
                title
            )


            all_news.append({

                "title": title,

                "link": link,

                "source": source_name,

                "category": category,

                "language": language

            })


    except Exception as e:

        print(
            "Hiba:",
            e
        )


# -----------------------------
# Mentés
# -----------------------------

with open(
    "news.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_news,
        f,
        ensure_ascii=False,
        indent=2
    )


print("\n----------------")
print(
    f"Kész: {len(all_news)} hír mentve"
)
print("----------------")

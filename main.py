import feedparser
import json
from urllib.parse import urlparse

# RSS források beolvasása

with open("sources.txt", "r", encoding="utf-8") as file:
    sources = [
        line.strip()
        for line in file.readlines()
        if line.strip() and not line.startswith("#")
    ]


all_news = []


# Egyszerű nyelv felismerés RSS alapján
def detect_language(url):
    if any(x in url for x in [
        "telex.hu",
        "hvg.hu",
        "24.hu",
        "portfolio.hu"
    ]):
        return "hu"

    return "en"


# Forrás neve kinyerése
def get_source(url):
    domain = urlparse(url).netloc.replace("www.", "")

    names = {
        "theverge.com": "The Verge",
        "techcrunch.com": "TechCrunch",
        "technologyreview.com": "MIT Technology Review",
        "arstechnica.com": "Ars Technica",
        "hnrss.org": "Hacker News",
        "nature.com": "Nature",
        "science.org": "Science",
        "newscientist.com": "New Scientist",
        "sciencedaily.com": "ScienceDaily",
        "telex.hu": "Telex",
        "hvg.hu": "HVG",
        "24.hu": "24.hu",
        "bbc.co.uk": "BBC",
        "dw.com": "DW",
        "theguardian.com": "The Guardian",
        "portfolio.hu": "Portfolio",
        "wsj.com": "Wall Street Journal"
    }

    return names.get(domain, domain)



for url in sources:
    print(f"\nOlvasom: {url}")

    try:
        feed = feedparser.parse(url)

        source = get_source(url)
        language = detect_language(url)

        for entry in feed.entries[:5]:

            title = entry.get("title", "Nincs cím")
            link = entry.get("link", "")

            all_news.append({
                "title": title,
                "source": source,
                "language": language,
                "link": link
            })


    except Exception as e:
        print("Hiba:", e)



print("\n\n===== HÍREK =====\n")

for i, news in enumerate(all_news, 1):
    print(
        f"{i}. {news['title']} "
        f"({news['source']} - {news['language']})"
    )
    print(news["link"])
    print()



# JSON mentés

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(
        all_news,
        f,
        ensure_ascii=False,
        indent=2
    )


print("\nMentve: news.json")

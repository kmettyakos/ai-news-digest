import feedparser
import json
from urllib.parse import urlparse


# Forrás nyelvének felismerése

def get_language(url):
    hungarian_sources = [
        "telex.hu",
        "hvg.hu",
        "24.hu",
        "portfolio.hu"
    ]

    for site in hungarian_sources:
        if site in url:
            return "hu"

    return "en"


# Forrás nevének felismerése

def get_source_name(url):
    domain = urlparse(url).netloc

    names = {
        "www.theverge.com": "The Verge",
        "techcrunch.com": "TechCrunch",
        "www.technologyreview.com": "MIT Technology Review",
        "feeds.arstechnica.com": "Ars Technica",
        "hnrss.org": "Hacker News",
        "www.nature.com": "Nature",
        "www.science.org": "Science",
        "www.newscientist.com": "New Scientist",
        "www.sciencedaily.com": "ScienceDaily",
        "telex.hu": "Telex",
        "hvg.hu": "HVG",
        "24.hu": "24.hu",
        "feeds.bbci.co.uk": "BBC",
        "rss.dw.com": "DW",
        "www.theguardian.com": "The Guardian",
        "www.portfolio.hu": "Portfolio",
        "feeds.a.dj.com": "Wall Street Journal"
    }

    return names.get(domain, domain)


# RSS források beolvasása

with open("sources.txt", "r", encoding="utf-8") as file:
    sources = [
        line.strip()
        for line in file.readlines()
        if line.strip() and not line.startswith("#")
    ]


all_news = []


for url in sources:
    print(f"\nOlvasom: {url}")

    try:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:

            title = entry.get("title", "Nincs cím")
            link = entry.get("link", "")

            all_news.append({
                "title": title,
                "link": link,
                "source": get_source_name(url),
                "language": get_language(url)
            })

    except Exception as e:
        print("Hiba:", e)



print("\n\n===== HÍREK =====\n")

for i, news in enumerate(all_news, 1):
    print(f"{i}. {news['title']}")
    print(f"Forrás: {news['source']}")
    print(f"Nyelv: {news['language']}")
    print(news["link"])
    print()


# JSON mentése

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(all_news, f, ensure_ascii=False, indent=2)


print("\nMentve: news.json")

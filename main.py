import feedparser

# RSS források beolvasása
with open("sources.txt", "r") as file:
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
                "link": link
            })

    except Exception as e:
        print("Hiba:", e)


print("\n\n===== HÍREK =====\n")

for i, news in enumerate(all_news, 1):
    print(f"{i}. {news['title']}")
    print(news["link"])
    print()

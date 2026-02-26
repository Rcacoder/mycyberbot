import feedparser
import datetime
import logging
from typing import List, Dict

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Popular Cybersecurity RSS feeds
RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.cisa.gov/uscert/ncas/alerts.xml",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml"
]

def fetch_daily_news() -> List[Dict[str, str]]:
    """Fetches articles from RSS feeds published in the last 24 hours."""
    articles = []
    
    # Calculate cutoff time: 24 hours ago
    cutoff_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    
    for feed_url in RSS_FEEDS:
        logging.info(f"Fetching from {feed_url}")
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                # Some feeds might not have a published_parsed attribute, fall back to updated_parsed
                entry_date_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
                
                if entry_date_parsed:
                    # Convert time.struct_time to datetime
                    entry_date = datetime.datetime(*entry_date_parsed[:6], tzinfo=datetime.timezone.utc)
                    
                    if entry_date >= cutoff_time:
                        articles.append({
                            "title": entry.get("title", ""),
                            "link": entry.get("link", ""),
                            "description": entry.get("summary", "") or entry.get("description", ""),
                            "source": feed.feed.get("title", feed_url),
                            "date": entry_date.isoformat()
                        })
        except Exception as e:
            logging.error(f"Error fetching from {feed_url}: {e}")
            
    logging.info(f"Total articles fetched from last 24 hours: {len(articles)}")
    return articles

if __name__ == "__main__":
    # Test the fetcher independently
    fetched_articles = fetch_daily_news()
    for article in fetched_articles[:3]:
        print(f"[{article['source']}] {article['title']}\n{article['link']}\n")

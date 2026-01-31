import re
import requests
import xml.etree.ElementTree as ET
from config.constants import Constants

def _strip_html(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&amp;', '&').replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>').replace('&nbsp;', ' ')
    return text.strip()

def fetch_rss(url, source_name, limit=5):
    print(f"Fetching from: {source_name}...")
    try:
        response = requests.get(url, headers=Constants.USER_AGENT, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return []

        root = ET.fromstring(response.content)
        news_items = []
        count = 0
        
        for item in root.findall('.//item'):
            if count >= limit:
                break
            
            title_node = item.find('title')
            link_node = item.find('link')
            source_node = item.find('source')
            
            title = title_node.text if title_node is not None else ""
            link = link_node.text if link_node is not None else ""
            publisher = source_node.text if source_node is not None else source_name
            
            if not title or not link:
                continue
            
            news_items.append(f"[{publisher}] {title} | Link: {link}")
            count += 1
            
        return news_items

    except Exception as e:
        print(f"Error fetching {source_name}: {str(e)}")
        return []

def get_aggregated_news():
    all_news = []
    for url, name, limit in Constants.NEWS_SOURCES:
        all_news.extend(fetch_rss(url, name, limit))

    if not all_news:
        return None
        
    return "\n---\n".join(all_news)
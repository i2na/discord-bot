import requests
import xml.etree.ElementTree as ET
from config.constants import Constants

def fetch_rss(url, source_name, limit=5):
    print(f"Fetching from: {source_name}...")
    try:
        response = requests.get(url, headers=Constants.USER_AGENT, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return []

        root = ET.fromstring(response.content)
        news_items = []
        count = 0
        
        for item in root.findall('.//item'):
            if count >= limit: break
            
            title = item.find('title').text
            link = item.find('link').text
            
            desc_node = item.find('description')
            description = desc_node.text if desc_node is not None else ""
            
            if description:
                description = description.replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('<![CDATA[', '').replace(']]>', '')
                if len(description) > 300: description = description[:300] + "..."
            
            news_items.append(f"[Source: {source_name}] Title: {title} | Link: {link} | Summary: {description}")
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
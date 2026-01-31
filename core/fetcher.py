import requests
import xml.etree.ElementTree as ET
from .interfaces import Fetcher


USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}


class RSSFetcher(Fetcher):
    def fetch(self, sources: list) -> str:
        all_news = []
        for url, name, limit in sources:
            items = self._fetch_rss(url, name, limit)
            all_news.extend(items)

        if not all_news:
            return None

        return "\n---\n".join(all_news)

    def _fetch_rss(self, url: str, source_name: str, limit: int = 5) -> list:
        print(f"Fetching from: {source_name}...")
        try:
            response = requests.get(url, headers=USER_AGENT, timeout=15)
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

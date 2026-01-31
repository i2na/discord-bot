from http.server import BaseHTTPRequestHandler
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.fetcher import get_aggregated_news
from services.analyst import analyze_news
from services.notifier import send_to_discord

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print("Mission Start.")
            news_data = get_aggregated_news()
            
            if news_data:
                report = analyze_news(news_data)
                status = send_to_discord(report)
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f'Mission Complete: {status}'.encode('utf-8'))
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write('Mission Failed: No news found.'.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))
        return
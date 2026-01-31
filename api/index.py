from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bots.registry import get_bot, BotRegistry


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            query_params = parse_qs(parsed.query)
            bot_name = query_params.get('bot', [None])[0]

            if not bot_name:
                self.send_response(400)
                self.end_headers()
                available = BotRegistry.list_bots()
                self.wfile.write(f'Missing parameter: bot. Available: {available}'.encode('utf-8'))
                return

            try:
                bot = get_bot(bot_name)
            except KeyError as e:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
                return

            result = bot.run()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(f'Bot [{bot_name}] completed: {result}'.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))

import requests
import datetime
from config.constants import Constants

def send_to_discord(content):
    webhook_url = Constants.DISCORD_WEBHOOK_URL
    
    if not webhook_url:
        return "Error: Webhook URL missing"
        
    today = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    
    header_msg = f"# 📰 {today} 시사 브리핑\n오늘 꼭 알아야 할 뉴스 5가지를 정리해 드립니다.\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    final_content = header_msg + content
    
    chunk_size = Constants.MAX_MESSAGE_LENGTH
    chunks = [final_content[i:i+chunk_size] for i in range(0, len(final_content), chunk_size)]
    
    for chunk in chunks:
        data = {
            "content": chunk,
            "username": Constants.BOT_NAME,
            "avatar_url": Constants.BOT_AVATAR_URL
        }
        try:
            requests.post(webhook_url, json=data)
        except Exception as e:
            return f"Transmission Failed: {str(e)}"
            
    return "Report Sent Successfully"
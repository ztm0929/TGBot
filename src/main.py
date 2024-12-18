import requests
from bs4 import BeautifulSoup
import json
from telegram import Bot
import asyncio
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# 添加环境变量检查
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("请确保设置了 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID 环境变量")

# 打印检查
print(f"Chat ID: {TELEGRAM_CHAT_ID}")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

URL = "http://www.sz.gov.cn/cn/xxgk/zfxxgj/gqdt/index.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def read_old_news():
    try:
        with open("news.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_new_news(new_news):
    with open("news.json", "w", encoding="utf-8") as file:
        json.dump(new_news, file, ensure_ascii=False, indent=4)

async def check_news():
    response = requests.get(URL, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    news_items = soup.find("div", class_="zx_ml_list")
    news_items = news_items.find_all("li")

    old_news = read_old_news()

    new_news = []
    for item in news_items:
        title_tag = item.find("a")
        if title_tag:
            title = title_tag.text
            link = title_tag["href"]

            if title not in [n['title'] for n in old_news]:
                new_news.append({"title": title, "link": link})   
    
    if new_news:
        for news in new_news:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"{news['title']}\n{news['link']}")

        old_news.extend(new_news)
        save_new_news(old_news)
    else:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="No new news found.")

asyncio.run(check_news())





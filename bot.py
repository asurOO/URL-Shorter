import os, requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = Bot(token=BOT_TOKEN)
DP = Dispatcher()

@DP.message(Command("start"))
async def cmd_start(msg: types.Message):
    await msg.reply("Send me a URL, I'll return a short version!")

@DP.message()
async def shorten(msg: types.Message):
    url = msg.text.strip()
    resp = requests.post(f"https://{os.getenv('DOMAIN')}/_new", json={"url": url})
    if resp.ok:
        j = resp.json()
        await msg.reply(f"✅ Short URL: {j['short_url']}")
    else:
        await msg.reply("❌ Invalid URL or error.")

if __name__ == "__main__":
    import asyncio
    from aiogram import executor
    executor.start_polling(DP, skip_updates=True)
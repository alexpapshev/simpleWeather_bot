import asyncio
import logging
import aiohttp
from aiogram import F, Bot, Dispatcher, types
from config import BOT_TOKEN, WEATHER_API_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def get_weather(city: str):
    """
    This function will return the current weather at the given city.
    If any error occurs, it will return None.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url = "https://api.openweathermap.org/data/2.5/weather",
            params = {
                "q": city,
                "appid": WEATHER_API_TOKEN,},
        ) as response:
            data = await response.json()
            return data["weather"][0]["description"]


@dp.message(F.text.startswith("/start "))
async def start(message: types.Message):
    weather_location = message.text.replace("/start", "")
    weather = await get_weather(city=weather_location)
    await message.reply(f"Your choice: {weather}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(dp.run_polling(bot))
    except Exception as ex:
        print("Bot is closed.")

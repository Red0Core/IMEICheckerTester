from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from .config import TOKEN_BOT
from tg_bot import imei_router

async def main():
    # Создание бота
    bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(imei_router.router)

    # Запуск polling
    await dp.start_polling(bot)

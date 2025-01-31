from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from logger import logger
from database import get_db, User, SessionLocal
from services.imei_checker import get_imei_info, IMEI
import asyncio

from tg_bot.config import ADMINS

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        text=f"Пришли мне IMEI после команды /imei и я дам тебе его описание, если ты в WL."
             f"Ваш id={message.from_user.id} для обращения к админам"
    )

def is_allowed_user(tg_user_id) -> bool:
    db = SessionLocal()
    user = db.query(User).filter(tg_user_id == User.telegram_id).first()
    db.close()
    return user is not None

def format_imei(response) -> str:
    return str(response)

@router.message(Command("imei"))
async def imei_handler(message: Message):
    if is_allowed_user(message.from_user.id):
        arr = message.text.split(maxsplit=1)
        if len(arr) == 1:
            await message.answer("После /imei напишите ваш IMEI")
        else:
            try:
                imei = IMEI(imei=arr[1])
                await message.answer(
                    format_imei(
                        get_imei_info(
                            imei
                        )
                    )
                )
            except ValueError:
                await message.answer("Не корректен ваш IMEI")

@router.message(Command("add_wl"))
async def add_user_to_wl(message: Message):
    if message.from_user.id in ADMINS:
        arr = message.text.split(maxsplit=1)
        if len(arr) == 1:
            await message.answer("Чтобы добавить в wl напишите после '/add_wl' id телеграмма пользователя")
        else:
            id_to_wl = arr[1]
            db = SessionLocal()
            
            user = db.query(User).filter(User.telegram_id == id_to_wl).first()
            if user:
                await message.answer("✅ Пользователь уже в белом списке.")
            else:
                new_user = User(telegram_id=id_to_wl)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                await message.answer(f"✅ Пользователь `{id_to_wl}` добавлен в WL.")

            db.close()
    else:
        await message.answer("Вы не админ!")

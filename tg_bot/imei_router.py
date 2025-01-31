from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from logger import logger
from database import User, SessionLocal
from services.imei_checker import get_imei_info, IMEI
from datetime import datetime

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
    try:
        user = db.query(User).filter(User.telegram_id == tg_user_id).first()
    finally:
        db.close()
    return user is not None

def format_imei(device_info) -> str:
    if "errors" in device_info:
        message = str(device_info)
    else:
        # Преобразуем timestamp в дату
        timestamp = device_info.get('properties', {}).get('estPurchaseDate')
        if timestamp:
            est_purchase_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            est_purchase_date = "N/A"
        processed_at = datetime.fromtimestamp(device_info.get('processedAt', 0)).strftime('%Y-%m-%d %H:%M:%S')
        message = f"""
<b>Device Name:</b> {device_info.get('properties', {}).get('deviceName', 'N/A')}
<b>IMEI:</b> {device_info.get('properties', {}).get('imei', 'N/A')}
<b>Serial:</b> {device_info.get('properties', {}).get('serial', 'N/A')}
<b>IMEI2:</b> {device_info.get('properties', {}).get('imei2', 'N/A')}
<b>MEID:</b> {device_info.get('properties', {}).get('meid', 'N/A')}

<b>Purchase Date:</b> {est_purchase_date}
<b>Apple Region:</b> {device_info.get('properties', {}).get('apple/region', 'N/A')}
<b>Apple Model Name:</b> {device_info.get('properties', {}).get('apple/modelName', 'N/A')}
<b>Network:</b> {device_info.get('properties', {}).get('network', 'N/A')}
<b>USA Block Status:</b> {device_info.get('properties', {}).get('usaBlockStatus', 'N/A')}

<b>Warranty Status:</b> {device_info.get('properties', {}).get('warrantyStatus', 'N/A')}
<b>Repair Coverage:</b> {'Yes' if device_info.get('properties', {}).get('repairCoverage') else 'No'}
<b>Demo Unit:</b> {'Yes' if device_info.get('properties', {}).get('demoUnit') else 'No'}
<b>Refurbished:</b> {'Yes' if device_info.get('properties', {}).get('refurbished') else 'No'}
<b>Replacement:</b> {'Yes' if device_info.get('properties', {}).get('replaced') else 'No'}
<b>Lost Mode:</b> {'Yes' if device_info.get('properties', {}).get('gsmaBlacklisted') else 'No'}

<b>Processed At:</b> {processed_at}
<b>Device Image:</b> <a href="{device_info.get('properties', {}).get('image', '')}">View Image</a>
    """

    return message


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
                        await get_imei_info(
                            imei
                        )
                    ), parse_mode="HTML"
                )
            except ValueError:
                logger.exception(f"Ошибка IMEI: {message.text}")
                await message.answer("Не корректен ваш IMEI")
    else:
        await message.answer(f"Вы не в WL. Обратить к администратору с вашим id={message.from_user.id}")

@router.message(Command("add_wl"))
async def add_user_to_wl(message: Message):
    if message.from_user.id in ADMINS:
        arr = message.text.split(maxsplit=1)
        if len(arr) == 1:
            await message.answer("Чтобы добавить в wl напишите после '/add_wl' id телеграмма пользователя")
        else:
            try:
                id_to_wl = int(arr[1])
            except ValueError:
                logger.exception(f"Ошибка wl: {message.text}")
                await message.answer(f"ID должен быть числом!")
                return

            db = SessionLocal()
            try:
                user = db.query(User).filter(User.telegram_id == id_to_wl).first()
                if user:
                    await message.answer("✅ Пользователь уже в белом списке.")
                else:
                    new_user = User(telegram_id=id_to_wl)
                    db.add(new_user)
                    db.commit()
                    db.refresh(new_user)
                    await message.answer(f"✅ Пользователь `{id_to_wl}` добавлен в WL.")
            finally:
                db.close()
    else:
        await message.answer("Вы не админ!")

from fastapi import Depends, APIRouter
from database import get_db, User
from sqlalchemy.orm import Session
from routers.auth import get_current_user
from ..imei_checker import IMEI, get_imei_info

router = APIRouter()

@router.post(
        "/check-imei",
        status_code=200,
        summary="Информация о IMEI",
        description="Проверяет через сервис imeicheck.net IMEI пользователя"
    )
async def check_imei(imei: IMEI, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_imei_info(imei)

from fastapi import Depends, APIRouter
from pydantic import BaseModel
from database import User
from .auth import get_current_user
from services.imei_checker import IMEI, get_imei_info

router = APIRouter()

class IMEIResponse(BaseModel):
    status: str
    data: dict | None = None
    error: str | None = None

@router.post(
        "/check-imei",
        status_code=200,
        summary="Информация о IMEI",
        description="Проверяет через сервис imeicheck.net IMEI пользователя"
    )
async def check_imei(imei: IMEI, user: User = Depends(get_current_user)) -> IMEIResponse:
    result = await get_imei_info(imei)
    if result.get("errors"):
        return IMEIResponse(status="error", error=result["errors"])
    else:
        return IMEIResponse(status="successful", data=result['properties'])

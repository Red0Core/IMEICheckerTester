import httpx
from pydantic import BaseModel, field_validator, Field

class IMEI(BaseModel):
    imei: str = Field(..., min_length=15, max_length=15)

    @field_validator('imei', mode='after')
    @classmethod
    def is_imei_valid(cls, value: str) -> str:
        """Проверяет IMEI на корректность"""
        if not all((str.isdigit(x) for x in value)):
            raise ValueError(f'IMEI has only digits')

        if int(value[-1]) != cls.luhn_checksum(value[:14]): # Проверка на корректность
            raise ValueError(f'{value} is not an IMEI')
        return value  

    @staticmethod
    def luhn_checksum(imei_part: str) -> int:
        """Выдает чексумму по алгоритма Луна"""
        digits = [int(d) for d in imei_part]
        checksum = 0
        for id, num in enumerate(digits):
            if (id+1) % 2 == 0:  # Четные позиции (по 0-индексации) удваиваются
                num *= 2
                if num > 9:
                    num -= 9
            checksum += num
        
        return (10 - (checksum % 10)) % 10 # Контрольная цифра


def get_imei_info(imei: IMEI) -> dict:
    # Временное решение для тестов
    return mock_get_imei_info(imei)

def mock_get_imei_info(imei: IMEI) -> dict:
    """Пример ответа API imeicheck.net"""
    return {
        "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
        "type": "api",
        "status": "successful",
        "orderId": "",
        "service": {
            "id": 1,
            "title": "Apple Basic Info"
        },
        "amount": "0.14",
        "deviceId": "123456789012345",
        "processedAt": 41241252112,
        "properties": {
            "deviceName": "iPhone 11 Pro",
            "image": "https://sources.imeicheck.net/image.jpg",
            "imei": "123456789012345",
            "estPurchaseDate": 1422349078,
            "simLock": True,
            "warrantyStatus": "AppleCare Protection Plan",
            "repairCoverage": "false",
            "technicalSupport": "false",
            "modelDesc": "IPHONE 12 BLACK 64GB-JPN",
            "demoUnit": True,
            "refurbished": True,
            "purchaseCountry": "Thailand",
            "apple/region": "AT&T USA",
            "fmiOn": True,
            "lostMode": "false",
            "usaBlockStatus": "Clean",
            "network": "Global"
        }
    }

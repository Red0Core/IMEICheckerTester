from services.imei_checker import IMEI, mock_get_imei_info
from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest
from pydantic import ValidationError

def test_imei_checker():
    assert(IMEI(imei="354190023896443") is not None)

@patch("services.imei_checker.get_imei_info", side_effect=mock_get_imei_info)
def test_check_imei(mock_api, client: TestClient, clean_database, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/check-imei", json={"imei": "490154203237518"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "successful"

def test_invalid_imei_non_digit():
    with pytest.raises(ValidationError) as exc_info:
        IMEI(imei="490154BCG323751")
    assert "IMEI has only digits" in str(exc_info.value)

def test_invalid_imei_wrong_length():
    with pytest.raises(ValidationError):
        IMEI(imei="49015420323751")  # 14 цифр
    with pytest.raises(ValidationError):
        IMEI(imei="4901542032375188")  # 16 цифр

def test_invalid_imei_checksum():
    # Изменяем контрольную цифру, чтобы получить неверный IMEI
    with pytest.raises(ValidationError) as exc_info:
        IMEI(imei="490154203237517")
    assert "is not an IMEI" in str(exc_info.value)

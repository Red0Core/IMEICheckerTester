from services.imei_checker import IMEI, mock_get_imei_info
from unittest.mock import patch
from fastapi.testclient import TestClient

def test_imei_checker():
    assert(IMEI(imei="354190023896443") is not None)

@patch("backend.imei_checker.get_imei_info", side_effect=mock_get_imei_info)
def test_check_imei(mock_api, client: TestClient, clean_database, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/check-imei", json={"imei": "490154203237518"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "successful"

from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from tests.mocks import bodies
from tests.mocks.db_responses import TestCompany
from tests.mocks.constants import TEST_COMPANY_ID


def test_create_company_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_company = TestCompany()

    mocker.patch("views.company.operations.create_company", return_value=TestCompany())
    response = client_with_auth.post("/v1/company", json=bodies.create_company_request())

    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert json_response == mock_db_company.properties


def test_get_company_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_company = TestCompany()

    mocker.patch("views.company.operations.get_company", return_value=TestCompany())
    response = client_with_auth.get(f"/v1/company/{TEST_COMPANY_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == mock_db_company.properties


def test_create_company_failed_bad_request(client_with_auth: TestClient):
    response = client_with_auth.post("/v1/company", json=bodies.create_company_request().pop("type"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert json_response == {
        "responseCode": "BAD_REQUEST",
        "responseMessage": (
            "Invalid request (('body',)): Input should be a valid dictionary or object to extract fields from"
        ),
    }

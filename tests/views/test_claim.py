from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from tests.mocks import bodies
from tests.mocks.db_responses import TestClaim
from tests.mocks.constants import TEST_CLAIM_ID


def test_create_claim_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_claim = TestClaim()

    mocker.patch("views.claim.operations.create_claim", return_value=TestClaim())
    response = client_with_auth.post("/v1/claim", json=bodies.create_claim_request())

    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert json_response == mock_db_claim.properties


def test_get_claim_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_claim = TestClaim()

    mocker.patch("views.claim.operations.get_claim", return_value=TestClaim())
    response = client_with_auth.get(f"/v1/claim/{TEST_CLAIM_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == mock_db_claim.properties


def test_create_claim_failed_bad_request(client_with_auth: TestClient):
    response = client_with_auth.post("/v1/claim", json=bodies.create_claim_request().pop("amount"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert json_response == {
        "responseCode": "BAD_REQUEST",
        "responseMessage": (
            "Invalid request (('body',)): Input should be a valid dictionary or object to extract fields from"
        ),
    }

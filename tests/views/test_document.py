from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from tests.mocks import bodies
from tests.mocks.db_responses import TestDocument
from tests.mocks.constants import TEST_DOCUMENT_ID


def test_create_document_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_document = TestDocument()

    mocker.patch("views.document.operations.create_document", return_value=TestDocument())
    response = client_with_auth.post("/v1/document", json=bodies.create_document_request())

    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert json_response == mock_db_document.properties


def test_get_document_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_document = TestDocument()

    mocker.patch("views.document.operations.get_document", return_value=TestDocument())
    response = client_with_auth.get(f"/v1/document/{TEST_DOCUMENT_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == mock_db_document.properties


def test_create_document_failed_bad_request(client_with_auth: TestClient):
    response = client_with_auth.post("/v1/document", json=bodies.create_document_request().pop("submission_date"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert json_response == {
        "responseCode": "BAD_REQUEST",
        "responseMessage": (
            "Invalid request (('body',)): Input should be a valid dictionary or object to extract fields from"
        ),
    }

from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from tests.mocks import bodies
from tests.mocks.db_responses import TestPerson
from tests.mocks.constants import TEST_PERSON_ID


def test_create_person_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_person = TestPerson()

    mocker.patch("views.person.operations.create_person", return_value=TestPerson())
    response = client_with_auth.post("/v1/person", json=bodies.create_person_request())

    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert json_response == mock_db_person.properties


def test_get_person_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_person = TestPerson()

    mocker.patch("views.person.operations.get_person", return_value=TestPerson())
    response = client_with_auth.get(f"/v1/person/{TEST_PERSON_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == mock_db_person.properties


def test_create_person_failed_bad_request(client_with_auth: TestClient):
    response = client_with_auth.post("/v1/person", json=bodies.create_person_request().pop("name"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert json_response == {
        "responseCode": "BAD_REQUEST",
        "responseMessage": (
            "Invalid request (('body',)): Input should be a valid dictionary or object to extract fields from"
        ),
    }

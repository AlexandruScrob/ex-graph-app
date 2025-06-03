from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from tests.mocks.db_responses import TestCompany, TestClaim
from tests.mocks.constants import TEST_COMPANY_ID, TEST_PERSON_ID, TEST_CLAIM_ID, TEST_DOCUMENT_ID


def test_create_person_company_relationship_success(client_with_auth: TestClient, mocker: MockerFixture):
    mocker.patch("views.company.operations.create_person_company_relationship", return_value=True)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/company/{TEST_COMPANY_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == f"SUCCESS Person with id:{TEST_PERSON_ID} WORKS FOR company with id:{TEST_COMPANY_ID}"


def test_create_person_claim_relationship_success(client_with_auth: TestClient, mocker: MockerFixture):
    mocker.patch("views.company.operations.create_person_claim_relationship", return_value=True)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/claim/{TEST_CLAIM_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == f"SUCCESS Person with id:{TEST_PERSON_ID} SUBMITTED claim with id:{TEST_CLAIM_ID}"


def test_create_person_document_relationship_success(client_with_auth: TestClient, mocker: MockerFixture):
    mocker.patch("views.company.operations.create_person_document_relationship", return_value=True)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/document/{TEST_DOCUMENT_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == f"SUCCESS Person with id:{TEST_PERSON_ID} SENT document with id:{TEST_DOCUMENT_ID}"


def test_get_claims_by_person_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_claim_1 = TestClaim(claim_id="f3055331-8486-4db4-8840-2d03266969dd")
    mock_db_claim_2 = TestClaim(claim_id="f4055331-8486-4db4-8840-2d03266969dd")

    mocker.patch(
        "views.company.operations.get_claims_by_person",
        return_value=[mock_db_claim_1, mock_db_claim_2],
    )
    response = client_with_auth.get(f"/v1/person/{TEST_PERSON_ID}/claims")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == [mock_db_claim_1.properties, mock_db_claim_2.properties]


def test_get_claims_by_company_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_claim_1 = TestClaim(claim_id="f3055331-8486-4db4-8840-2d03266969dd")
    mock_db_claim_2 = TestClaim(claim_id="f4055331-8486-4db4-8840-2d03266969dd")

    mocker.patch(
        "views.company.operations.get_claims_by_company",
        return_value=[mock_db_claim_1, mock_db_claim_2],
    )
    response = client_with_auth.get(f"/v1/claims/company/{TEST_COMPANY_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == [mock_db_claim_1.properties, mock_db_claim_2.properties]


def test_get_company_by_person_success(client_with_auth: TestClient, mocker: MockerFixture):
    mock_db_company = TestCompany()
    mocker.patch("views.company.operations.get_company_by_person", return_value=mock_db_company)
    response = client_with_auth.get(f"/v1/company/person/{TEST_PERSON_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == mock_db_company.properties


def test_create_person_company_relationship_failed(client_with_auth: TestClient, mocker: MockerFixture):
    mocker.patch("views.company.operations.create_person_company_relationship", return_value=False)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/company/{TEST_COMPANY_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == f"FAILED Person with id:{TEST_PERSON_ID} WORKS FOR company with id:{TEST_COMPANY_ID}"


def test_create_person_claim_relationship_failed(client_with_auth: TestClient, mocker: MockerFixture):
    mocker.patch("views.company.operations.create_person_claim_relationship", return_value=False)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/claim/{TEST_CLAIM_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == f"FAILED Person with id:{TEST_PERSON_ID} SUBMITTED claim with id:{TEST_CLAIM_ID}"


def test_create_person_document_relationship_failed(client_with_auth: TestClient, mocker: MockerFixture):
    mocker.patch("views.company.operations.create_person_document_relationship", return_value=False)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/document/{TEST_DOCUMENT_ID}")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == f"FAILED Person with id:{TEST_PERSON_ID} SENT document with id:{TEST_DOCUMENT_ID}"

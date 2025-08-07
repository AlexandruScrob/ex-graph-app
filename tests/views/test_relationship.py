from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from structlog.testing import LogCapture

from core.logging.serializers import RequestContext
from tests.mocks.db_responses import TestCompany, TestClaim
from tests.mocks.constants import TEST_COMPANY_ID, TEST_PERSON_ID, TEST_CLAIM_ID, TEST_DOCUMENT_ID


def test_create_person_company_relationship_success(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mocker.patch("views.company.operations.create_person_company_relationship", return_value=True)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/company/{TEST_COMPANY_ID}")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["person"]["person_id"] == TEST_PERSON_ID
    assert log_out["person"]["method"] == "create_person_company_relationship"
    assert log_out["company"]["company_id"] == TEST_COMPANY_ID
    assert log_out["company"]["method"] == "create_person_company_relationship"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == (
        f"Successfully connected company with ID: {TEST_COMPANY_ID} with person with ID: {TEST_PERSON_ID}"
    )

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == {"isConnected": True}


def test_create_person_claim_relationship_success(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mocker.patch("views.company.operations.create_person_claim_relationship", return_value=True)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/claim/{TEST_CLAIM_ID}")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["person"]["person_id"] == TEST_PERSON_ID
    assert log_out["person"]["method"] == "create_person_claim_relationship"
    assert log_out["claim"]["claim_id"] == TEST_CLAIM_ID
    assert log_out["claim"]["method"] == "create_person_claim_relationship"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == (
        f"Successfully connected claim with ID: {TEST_CLAIM_ID} with person with ID: {TEST_PERSON_ID}"
    )

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == {"isConnected": True}


def test_create_person_document_relationship_success(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mocker.patch("views.company.operations.create_person_document_relationship", return_value=True)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/document/{TEST_DOCUMENT_ID}")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["person"]["person_id"] == TEST_PERSON_ID
    assert log_out["person"]["method"] == "create_person_document_relationship"
    assert log_out["document"]["document_id"] == TEST_DOCUMENT_ID
    assert log_out["document"]["method"] == "create_person_document_relationship"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == (
        f"Successfully connected document with ID: {TEST_DOCUMENT_ID} with person with ID: {TEST_PERSON_ID}"
    )

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == {"isConnected": True}


def test_get_claims_by_person_success(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mock_db_claim_1 = TestClaim(claim_id="f3055331-8486-4db4-8840-2d03266969dd")
    mock_db_claim_2 = TestClaim(claim_id="f4055331-8486-4db4-8840-2d03266969dd")

    mocker.patch(
        "views.company.operations.get_claims_by_person",
        return_value=[mock_db_claim_1, mock_db_claim_2],
    )
    response = client_with_auth.get(f"/v1/person/{TEST_PERSON_ID}/claims")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["person"]["person_id"] == TEST_PERSON_ID
    assert log_out["person"]["method"] == "get_claims_by_person"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == f"Successfully retrieved claims by person with ID: {TEST_PERSON_ID}"

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == [mock_db_claim_1.properties, mock_db_claim_2.properties]


def test_get_claims_by_company_success(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mock_db_claim_1 = TestClaim(claim_id="f3055331-8486-4db4-8840-2d03266969dd")
    mock_db_claim_2 = TestClaim(claim_id="f4055331-8486-4db4-8840-2d03266969dd")

    mocker.patch(
        "views.company.operations.get_claims_by_company",
        return_value=[mock_db_claim_1, mock_db_claim_2],
    )
    response = client_with_auth.get(f"/v1/claims/company/{TEST_COMPANY_ID}")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["company"]["company_id"] == TEST_COMPANY_ID
    assert log_out["company"]["method"] == "get_claims_by_company"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == f"Successfully retrieved claims by company with ID: {TEST_COMPANY_ID}"

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == [mock_db_claim_1.properties, mock_db_claim_2.properties]


def test_get_company_by_person_success(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mock_db_company = TestCompany()
    mocker.patch("views.company.operations.get_company_by_person", return_value=mock_db_company)
    response = client_with_auth.get(f"/v1/company/person/{TEST_PERSON_ID}")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["person"]["person_id"] == TEST_PERSON_ID
    assert log_out["person"]["method"] == "get_company_by_person"
    assert log_out["company"]["company_id"] == TEST_COMPANY_ID
    assert log_out["company"]["method"] == "get_company_by_person"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == (
        f"Successfully retrieved company with ID: {TEST_COMPANY_ID} by person with ID: {TEST_PERSON_ID}"
    )

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == mock_db_company.properties


def test_create_person_company_relationship_failed(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mocker.patch("views.company.operations.create_person_company_relationship", return_value=False)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/company/{TEST_COMPANY_ID}")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["person"]["person_id"] == TEST_PERSON_ID
    assert log_out["person"]["method"] == "create_person_company_relationship"
    assert log_out["company"]["company_id"] == TEST_COMPANY_ID
    assert log_out["company"]["method"] == "create_person_company_relationship"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == (
        f"Failed to connect company with ID: {TEST_COMPANY_ID} with person with ID: {TEST_PERSON_ID}"
    )

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == {"isConnected": False}


def test_create_person_claim_relationship_failed(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mocker.patch("views.company.operations.create_person_claim_relationship", return_value=False)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/claim/{TEST_CLAIM_ID}")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["person"]["person_id"] == TEST_PERSON_ID
    assert log_out["person"]["method"] == "create_person_claim_relationship"
    assert log_out["claim"]["claim_id"] == TEST_CLAIM_ID
    assert log_out["claim"]["method"] == "create_person_claim_relationship"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == (
        f"Failed to connect claim with ID: {TEST_CLAIM_ID} with person with ID: {TEST_PERSON_ID}"
    )

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == {"isConnected": False}


def test_create_person_document_relationship_failed(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mocker.patch("views.company.operations.create_person_document_relationship", return_value=False)
    response = client_with_auth.post(f"/v1/person/{TEST_PERSON_ID}/document/{TEST_DOCUMENT_ID}")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["person"]["person_id"] == TEST_PERSON_ID
    assert log_out["person"]["method"] == "create_person_document_relationship"
    assert log_out["document"]["document_id"] == TEST_DOCUMENT_ID
    assert log_out["document"]["method"] == "create_person_document_relationship"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == (
        f"Failed to connect document with ID: {TEST_DOCUMENT_ID} with person with ID: {TEST_PERSON_ID}"
    )

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == {"isConnected": False}

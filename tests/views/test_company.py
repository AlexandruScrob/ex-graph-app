from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from structlog.testing import LogCapture

from core.logging.serializers import RequestContext
from tests.mocks import bodies
from tests.mocks.db_responses import TestCompany
from tests.mocks.constants import TEST_COMPANY_ID


def test_create_company_success(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mock_db_company = TestCompany()

    mocker.patch("views.company.operations.create_company", return_value=TestCompany())
    response = client_with_auth.post("/v1/company", json=bodies.create_company_request())

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["company"]["company_id"] == TEST_COMPANY_ID
    assert log_out["company"]["method"] == "create_company"

    assert log_out["http"]["status_code"] == status.HTTP_201_CREATED

    assert log_out["level"] == "info"
    assert log_out["message"] == f"Successfully created company with ID: {TEST_COMPANY_ID}"

    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert json_response == mock_db_company.properties


def test_get_company_success(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mock_db_company = TestCompany()

    mocker.patch("views.company.operations.get_company", return_value=TestCompany())
    response = client_with_auth.get(f"/v1/company/{TEST_COMPANY_ID}")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["company"]["company_id"] == TEST_COMPANY_ID
    assert log_out["company"]["method"] == "get_company"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == f"Successfully retrieved company with ID: {TEST_COMPANY_ID}"

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == mock_db_company.properties


def test_create_company_failed_bad_request(
    client_with_auth: TestClient,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    response = client_with_auth.post("/v1/company", json=bodies.create_company_request().pop("type"))

    assert mocked_log_context.log.error is not None

    log_out = log_output.entries[0]
    assert log_out["http"]["status_code"] == status.HTTP_400_BAD_REQUEST

    assert log_out["level"] == "error"
    assert log_out["message"] == "Request Validation Error"

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert json_response == {
        "responseCode": "BAD_REQUEST",
        "responseMessage": (
            "Invalid request (('body',)): Input should be a valid dictionary or object to extract fields from"
        ),
    }

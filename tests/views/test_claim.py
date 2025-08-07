from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from structlog.testing import LogCapture

from core.logging.serializers import RequestContext
from tests.mocks import bodies
from tests.mocks.db_responses import TestClaim
from tests.mocks.constants import TEST_CLAIM_ID


def test_create_claim_success(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mock_db_claim = TestClaim()

    mocker.patch("views.claim.operations.create_claim", return_value=TestClaim())
    response = client_with_auth.post("/v1/claim", json=bodies.create_claim_request())

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["claim"]["claim_id"] == TEST_CLAIM_ID
    assert log_out["claim"]["method"] == "create_claim"

    assert log_out["http"]["status_code"] == status.HTTP_201_CREATED

    assert log_out["level"] == "info"
    assert log_out["message"] == f"Successfully created claim with ID: {TEST_CLAIM_ID}"

    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    assert json_response == mock_db_claim.properties


def test_get_claim_success(
    client_with_auth: TestClient,
    mocker: MockerFixture,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    mock_db_claim = TestClaim()

    mocker.patch("views.claim.operations.get_claim", return_value=TestClaim())
    response = client_with_auth.get(f"/v1/claim/{TEST_CLAIM_ID}")

    assert mocked_log_context.log.error is None

    log_out = log_output.entries[0]
    assert log_out["claim"]["claim_id"] == TEST_CLAIM_ID
    assert log_out["claim"]["method"] == "get_claim"

    assert log_out["http"]["status_code"] == status.HTTP_200_OK

    assert log_out["level"] == "info"
    assert log_out["message"] == f"Successfully retrieved claim with ID: {TEST_CLAIM_ID}"

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response == mock_db_claim.properties


def test_create_claim_failed_bad_request(
    client_with_auth: TestClient,
    log_output: LogCapture,
    mocked_log_context: RequestContext,
):
    response = client_with_auth.post("/v1/claim", json=bodies.create_claim_request().pop("amount"))

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

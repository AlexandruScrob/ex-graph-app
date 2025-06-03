from typing import Any

from tests.mocks.constants import TEST_PERSON_ID, TEST_CLAIM_ID, TEST_COMPANY_ID, TEST_DOCUMENT_ID


def create_person_request(person_id: str | None = None) -> dict[str, Any]:
    return {
        "pid": person_id or TEST_PERSON_ID,
        "name": "Test Name",
        "role": "test_role",
        "email": "test_email",
        "phone": "test_phone",
    }


def create_claim_request(claim_id: str | None = None) -> dict[str, Any]:
    return {
        "pid": claim_id or TEST_CLAIM_ID,
        "claim_number": "#12345",
        "amount": 1000.0,
        "status": "Submitted",
        "submission_date": "2025-05-27T16:02:08",
        "description": "test description",
    }


def create_company_request(company_id: str | None = None) -> dict[str, Any]:
    return {
        "pid": company_id or TEST_COMPANY_ID,
        "name": "Test company",
        "type": "Insurance",
        "registration_number": "23454",
        "address": "st. test",
    }


def create_document_request(document_id: str | None = None) -> dict[str, Any]:
    return {
        "pid": document_id or TEST_DOCUMENT_ID,
        "doc_number": "DOC12345",
        "submission_date": "2025-05-27T16:02:08",
        "content_type": "content",
        "file_path": "/file/path",
    }

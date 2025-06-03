from typing import Any

from tests.mocks.constants import TEST_PERSON_ID, TEST_DOCUMENT_ID, TEST_CLAIM_ID, TEST_COMPANY_ID


class TestPerson:
    def __init__(self, person_id: str | None = None) -> None:
        self.person_id = person_id or TEST_PERSON_ID

    @property
    def __properties__(self) -> dict[str, Any]:
        return {
            "pid": self.person_id or TEST_PERSON_ID,
            "name": "Test Name",
            "role": "test_role",
            "email": "test_email",
            "phone": "test_phone",
            "element_id_property": "4:03be8de5-020b-4edd-865a-24b8bfeaad20:24",
        }

    @property
    def properties(self) -> dict[str, Any]:
        return self.__properties__


class TestCompany:
    def __init__(self, company_id: str | None = None) -> None:
        self.company_id = company_id or TEST_COMPANY_ID

    @property
    def __properties__(self) -> dict[str, Any]:
        return {
            "pid": self.company_id or TEST_COMPANY_ID,
            "name": "Test company",
            "type": "Insurance",
            "registration_number": "23454",
            "address": "st. test",
            "element_id_property": "4:03be8de5-020b-4edd-865a-24b8bfeaad20:24",
        }

    @property
    def properties(self) -> dict[str, Any]:
        return self.__properties__


class TestClaim:
    def __init__(self, claim_id: str | None = None) -> None:
        self.claim_id = claim_id or TEST_CLAIM_ID

    @property
    def __properties__(self) -> dict[str, Any]:
        return {
            "pid": self.claim_id or TEST_CLAIM_ID,
            "claim_number": "#12345",
            "amount": 1000.0,
            "status": "Submitted",
            "submission_date": "2025-05-27T16:02:08",
            "description": "test description",
            "element_id_property": "4:03be8de5-020b-4edd-865a-24b8bfeaad20:24",
        }

    @property
    def properties(self) -> dict[str, Any]:
        return self.__properties__


class TestDocument:
    def __init__(self, document_id: str | None = None) -> None:
        self.document_id = document_id or TEST_DOCUMENT_ID

    @property
    def __properties__(self) -> dict[str, Any]:
        return {
            "pid": self.document_id or TEST_DOCUMENT_ID,
            "doc_number": "DOC12345",
            "submission_date": "2025-05-27T16:02:08",
            "content_type": "content",
            "file_path": "/file/path",
            "element_id_property": "4:03be8de5-020b-4edd-865a-24b8bfeaad20:24",
        }

    @property
    def properties(self) -> dict[str, Any]:
        return self.__properties__

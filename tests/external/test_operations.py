import pytest
from pytest_mock import MockerFixture

from external.neo4j.exceptions import EntityNotFoundError
from external.neo4j import operations

from tests.mocks.db_responses import TestPerson, TestClaim
from tests.mocks.constants import TEST_COMPANY_ID, TEST_PERSON_ID, TEST_CLAIM_ID


def test_create_person_company_relationship_failed_person_not_found(mocker: MockerFixture):
    mocker.patch("external.neo4j.operations.get_person", return_value=None)

    with pytest.raises(EntityNotFoundError) as exc:
        operations.create_person_company_relationship(person_id=TEST_PERSON_ID, company_id=TEST_COMPANY_ID)

    assert exc.value.args[0] == f"Person with id:{TEST_PERSON_ID} not found"


def test_create_person_company_relationship_failed_company_not_found(mocker: MockerFixture):
    mocker.patch("external.neo4j.operations.get_person", return_value=TestPerson())
    mocker.patch("external.neo4j.operations.get_company", return_value=None)

    with pytest.raises(EntityNotFoundError) as exc:
        operations.create_person_company_relationship(person_id=TEST_PERSON_ID, company_id=TEST_COMPANY_ID)

    assert exc.value.args[0] == f"Company with id:{TEST_COMPANY_ID} not found"


def test_create_person_claim_relationship_failed_person_not_found(mocker: MockerFixture):
    mocker.patch("external.neo4j.operations.get_person", return_value=None)

    with pytest.raises(EntityNotFoundError) as exc:
        operations.create_person_claim_relationship(person_id=TEST_PERSON_ID, claim_id=TEST_CLAIM_ID)

    assert exc.value.args[0] == f"Person with id:{TEST_PERSON_ID} not found"


def test_create_person_claim_relationship_failed_claim_not_found(mocker: MockerFixture):
    mocker.patch("external.neo4j.operations.get_person", return_value=TestPerson())
    mocker.patch("external.neo4j.operations.get_claim", return_value=None)

    with pytest.raises(EntityNotFoundError) as exc:
        operations.create_person_claim_relationship(person_id=TEST_PERSON_ID, claim_id=TEST_CLAIM_ID)

    assert exc.value.args[0] == f"Claim with id:{TEST_CLAIM_ID} not found"


def test_create_claim_company_relationship_failed_claim_not_found(mocker: MockerFixture):
    mocker.patch("external.neo4j.operations.get_claim", return_value=None)

    with pytest.raises(EntityNotFoundError) as exc:
        operations.create_claim_company_relationship(claim_id=TEST_CLAIM_ID, company_id=TEST_COMPANY_ID)

    assert exc.value.args[0] == f"Claim with id:{TEST_CLAIM_ID} not found"


def test_create_claim_company_relationship_failed_company_not_found(mocker: MockerFixture):
    mocker.patch("external.neo4j.operations.get_claim", return_value=TestClaim())
    mocker.patch("external.neo4j.operations.get_company", return_value=None)

    with pytest.raises(EntityNotFoundError) as exc:
        operations.create_claim_company_relationship(claim_id=TEST_CLAIM_ID, company_id=TEST_COMPANY_ID)

    assert exc.value.args[0] == f"Company with id:{TEST_COMPANY_ID} not found"


def test_get_claims_by_person_failed_claim_not_found(mocker: MockerFixture):
    mocker.patch("external.neo4j.operations.q.get_claims_by_person", return_value=None)

    with pytest.raises(EntityNotFoundError) as exc:
        operations.get_claims_by_person(person_id=TEST_PERSON_ID)

    assert exc.value.args[0] == f"No claims for person with id:{TEST_PERSON_ID} found"


def test_get_claims_by_company_failed_claim_not_found(mocker: MockerFixture):
    mocker.patch("external.neo4j.operations.q.get_claims_by_company", return_value=None)

    with pytest.raises(EntityNotFoundError) as exc:
        operations.get_claims_by_company(company_id=TEST_COMPANY_ID)

    assert exc.value.args[0] == f"No claims associated to Company with id:{TEST_COMPANY_ID} found"


def test_get_company_by_person_failed_claim_not_found(mocker: MockerFixture):
    mocker.patch("external.neo4j.operations.q.get_company_by_person", return_value=None)

    with pytest.raises(EntityNotFoundError) as exc:
        operations.get_company_by_person(person_id=TEST_PERSON_ID)

    assert exc.value.args[0] == f"Person with id:{TEST_PERSON_ID} is not assiociated with any Company"

import re
from datetime import datetime
from enum import StrEnum
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import SettingsConfigDict


class RelationshipType(StrEnum):
    WORKS_FOR = "WORKS_FOR"
    SUBMITTED = "SUBMITTED"
    SENT = "SENT"
    HAS_CLAIMANT = "HAS_CLAIMANT"


class CompanyType(StrEnum):
    INSURANCE = "Insurance"
    CLAIMANT = "Claimant"


class ClaimStatus(StrEnum):
    SUBMITTED = "Submitted"
    PROCESSING = "Processing"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class IDModel(BaseModel):
    """Base model with Id field and default uuid4 value"""

    model_config = SettingsConfigDict(use_enum_values=True)

    pid: Annotated[str, Field(default_factory=lambda: str(uuid4()))]


class Person(IDModel):
    name: str
    role: str | None = None
    email: str | None = None
    phone: str | None = None


class Company(IDModel):
    name: str
    type: CompanyType
    registration_number: str | None = None
    address: str | None = None


class Claim(IDModel):
    claim_number: str = Field(examples=["#1234"])
    amount: float
    status: ClaimStatus
    submission_date: datetime
    description: str | None = None

    @field_validator("claim_number", mode="before")
    @classmethod
    def validate_claim_number(cls, v: str) -> str:
        pattern = re.compile(r"^#[0-9]+$")
        if not pattern.match(v):
            raise ValueError("Invalid Claim Number. Valid example: '#1234'")
        return v


class Document(IDModel):
    doc_number: str = Field(examples=["DOC1234"])
    title: str | None = None
    submission_date: datetime
    content_type: str | None = None
    file_path: str | None = None

    @field_validator("doc_number")
    @classmethod
    def validate_doc_number(cls, v: str) -> str:
        pattern = re.compile(r"^DOC[0-9]+$")
        if not pattern.match(v):
            raise ValueError("Invalid Doc Number. Valid example: 'DOC1234'")
        return v

from pydantic import BaseModel, Field


class AuthorizationErrorResponse(BaseModel):
    """Response model for HTTP status code 401."""

    response_code: str = Field(alias="responseCode", default="UNAUTHORIZED")
    response_message: str = Field(
        alias="responseMessage",
        default="You have not provided adequate credentials to access this resource",
    )


class EntityNotFoundResponse(BaseModel):
    """Response model for EntityNotFoundError."""

    response_code: str = Field(alias="responseCode", default="NOT_FOUND")
    response_message: str = Field(alias="responseMessage", default="Entity not found")


class BadRequestResponse(BaseModel):
    """Response model for HTTP status code 400."""

    response_code: str = Field(alias="responseCode", default="BAD_REQUEST")
    response_message: str = Field(alias="responseMessage", default="Invalid request")

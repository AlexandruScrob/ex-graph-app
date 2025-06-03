from fastapi import HTTPException, status


class AuthorizationErrorException(HTTPException):
    def __init__(
        self,
        *args,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You have not provided adequate credentials to access this resource.",
        **kwargs,
    ):
        super().__init__(*args, status_code=status_code, detail=detail, **kwargs)

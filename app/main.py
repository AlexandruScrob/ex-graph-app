from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from core.exceptions import AuthorizationErrorException
from core.handlers import (
    catch_auth_exception,
    catch_entity_not_found,
    catch_request_validation_exception,
)
from core.logging.context import get_temporary_log_context, set_request_ctx_application_settings
from core.logging.logger import get_logger
from core.settings import get_settings
from external.neo4j.exceptions import EntityNotFoundError
from views.claim import router as claim_router
from views.company import router as company_router
from views.document import router as document_router
from views.person import router as person_router
from views.relationship import router as relationship_router

load_dotenv()
logger = get_logger()
settings = get_settings()


###
# Startup events
###
def _log_application_settings():
    """Log the application settings when the app starts to facilitate debugging."""

    # Make sure the context does not persist after "startup" event.
    with get_temporary_log_context():
        set_request_ctx_application_settings(settings)

        logger.info("Application settings")


###
# Startup Events
###
@asynccontextmanager
async def lifespan(app: FastAPI):
    from external.neo4j.operations import check_db_connection

    _log_application_settings()
    check_db_connection()

    # from external.neo4j.operations import clear_db

    # clear_db()
    yield


app = FastAPI(lifespan=lifespan)

###
# Include Routers
###
app.include_router(person_router, tags=["Person"])
app.include_router(company_router, tags=["Company"])
app.include_router(claim_router, tags=["Claim"])
app.include_router(document_router, tags=["Document"])
app.include_router(relationship_router, tags=["Relationships"])


###
# Register Handlers
###
app.add_exception_handler(AuthorizationErrorException, catch_auth_exception)
app.add_exception_handler(EntityNotFoundError, catch_entity_not_found)
app.add_exception_handler(RequestValidationError, catch_request_validation_exception)

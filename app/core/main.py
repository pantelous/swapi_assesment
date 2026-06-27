import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from app.core.config import settings
from app.core.db import _init
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api import character, film, starship
from app.core.config import settings
from app.core.exception import ApplicationException, DomainException
origins = ["*"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    _init()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    """Custom handler for request validation errors."""
    errors = []
    for err in exc.errors():
        if err["loc"][0] == "body":
            err["loc"] = err["loc"][1:]  # Remove 'body' from location

        errors.append(
            {
                "field": ".".join(str(x) for x in err["loc"] if isinstance(x, (str, int))),
                "message": err["msg"],
                "type": err["type"],
            }
        )

    return JSONResponse(
        status_code=422,
        content={"success": False, "error_type": "validation_error", "errors": errors},
    )


@app.exception_handler(DomainException)
async def domain_exception_handler(_request: Request, exc: DomainException):
    """Custom handler for domain exceptions."""
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error_type": exc.type,
            "errors": [
                {
                    "field": exc.field,
                    "message": exc.message,
                    "type": exc.type,
                    "error_code": exc.error_code,
                }
            ],
        },
    )



@app.exception_handler(ApplicationException)
async def application_exception_handler(_request: Request, exc: ApplicationException):
    """Custom handler for domain exceptions."""
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error_type": exc.type,
            "errors": [{"field": exc.field, "message": exc.message, "type": exc.type}],
        },
    )

app.include_router(character.router, prefix="/character", tags=["character"])
app.include_router(starship.router, prefix="/starship", tags=["starship"])
app.include_router(film.router, prefix="/film", tags=["film"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)
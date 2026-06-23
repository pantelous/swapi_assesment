import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.db import _init


@asynccontextmanager
async def lifespan(_: FastAPI):
    _init()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()

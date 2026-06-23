import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool, NullPool
from app.core.config import settings
from app.core.data_definition_language import run_data_definition_language

Base = declarative_base()
logger = logging.getLogger(__name__)

_engine = None
_sessionmaker = None


def _ensure_database_exists() -> None:
    """Connect to the default 'postgres' database and create the target DB if absent.

    CREATE DATABASE cannot run inside a transaction, so we use AUTOCOMMIT isolation.
    NullPool prevents connection reuse against the bootstrap database.
    """
    bootstrap_url = (
        f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
    )
    engine = create_engine(bootstrap_url, poolclass=NullPool)
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        exists = conn.execute(
            text("SELECT 1 FROM pg_catalog.pg_database WHERE datname = :name"),
            {"name": settings.DB_NAME},
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{settings.DB_NAME}"'))
            logger.info("Created database '%s'", settings.DB_NAME)
        else:
            logger.info("Database '%s' already exists — skipping creation", settings.DB_NAME)
    engine.dispose()


def _init() -> None:
    global _engine, _sessionmaker
    if _engine is not None:
        return

    logger.info(
        "DB init — user=%s host=%s port=%s dbname=%s",
        settings.DB_USER, settings.DB_HOST, settings.DB_PORT, settings.DB_NAME,
    )

    _ensure_database_exists()

    _engine = create_engine(
        f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
        poolclass=QueuePool,
        pool_size=settings.DB_MIN_POOL,
        max_overflow=settings.DB_MAX_POOL - settings.DB_MIN_POOL,
        pool_pre_ping=True,
    )

    run_data_definition_language(_engine)

    _sessionmaker = sessionmaker(
        bind=_engine,
        autoflush=False,
        autocommit=False,
        future=True,
    )


class LazySessionLocal:
    """Callable that behaves like sessionmaker but initialises the DB on first use."""

    def __call__(self, *args, **kwargs):
        _init()
        if _sessionmaker is None:
            raise RuntimeError("Failed to initialise database session maker")
        return _sessionmaker(*args, **kwargs)


SessionLocal = LazySessionLocal()

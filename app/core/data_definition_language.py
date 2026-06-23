import logging
from pathlib import Path
from sqlalchemy import text

logger = logging.getLogger(__name__)

_SQL_DIR = Path(__file__).parent / "sql"


def run_data_definition_language(engine) -> None:
    sql_files = sorted(_SQL_DIR.glob("*.sql"))
    with engine.begin() as conn:
        for path in sql_files:
            conn.execute(text(path.read_text()))
    logger.info("DB schema verified (%d statements)", len(sql_files))

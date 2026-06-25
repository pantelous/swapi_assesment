from sqlalchemy.orm import Session

from app.modules.character.domain.character.entity import Character
from app.modules.character.domain.repo.character_repo import CharacterRepoI


def load_character_id(session: Session, character_repo: CharacterRepoI, character_id: int) -> dict[str, int]:
    return character_repo.load_character_id(session, character_id)
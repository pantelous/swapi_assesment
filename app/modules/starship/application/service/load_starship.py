from app.modules.starship.domain.repo.starship_repo import StarshipRepoI


def load_starship_id(starship_repo: StarshipRepoI, starship_id: int) -> int:
    return starship_repo.load_starship_id(starship_id)

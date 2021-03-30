import os

from src import BASE_DIR


def get_db_location():
    return BASE_DIR / "testing_this_proj.db"


def get_db_uri():
    db_location = get_db_location().absolute()
    if os.name != "nt":
        db_location = f"/{db_location}"
    return f"sqlite:///{db_location}"

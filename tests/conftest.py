import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from tests.utils import get_db_location, get_db_uri


@pytest.fixture(autouse=True)
def _setup_database(request):
    if request.node.get_closest_marker("db"):
        location = get_db_location()
        location.unlink(missing_ok=True)
        yield
        location.unlink(missing_ok=True)
    else:
        yield


@pytest.fixture
def session() -> Session:
    engine = create_engine(get_db_uri())
    generate = sessionmaker(engine)
    yield generate()

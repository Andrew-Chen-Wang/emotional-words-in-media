import pytest
from dotenv import dotenv_values

from src import BASE_DIR
from src.extract import extract_youtube_videos
from src.models import Channel, Video
from tests.utils import get_db_uri


pytestmark = pytest.mark.db


class TestExtract:
    # I would do extensive testing... but I'm so lazy I can't be bothered... it's alr :P
    @property
    def channels(self):
        values = dotenv_values(BASE_DIR / ".env")
        DEFAULT_SHOULD_CHANGE = "https://www.youtube.com/playlist?list=CHANGE_THIS"
        return [values.get("TEST_PLAYLIST", DEFAULT_SHOULD_CHANGE)]

    @property
    def dk(self):
        return {"save_in_dolt": True, "db_uri": get_db_uri(), "setup_dolt": False}

    def test_extract(self, session):
        extract_youtube_videos(self.channels, **self.dk)
        assert session.query(Channel).count() == 1
        assert session.query(Video).count() == 1
        first_vid: Video = session.query(Video).first()

        # Test unique
        extract_youtube_videos(self.channels, **self.dk)
        assert session.query(Video).count() == 1
        updated_vid: Video = session.query(Video).first()
        assert updated_vid.record_created == first_vid.record_created

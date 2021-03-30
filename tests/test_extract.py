import pytest

from src.extract import extract_youtube_videos
from src.models import Channel, Video
from tests.utils import get_db_uri


pytestmark = pytest.mark.db


class TestExtract:
    # I would do extensive testing... but I'm so lazy I can't be bothered... it's alr :P
    channels = ["https://www.youtube.com/playlist?list=PRIVACY_REASONS"]

    @property
    def dk(self):
        return {"save-in-dolt": True, "db_uri": get_db_uri(), "setup_dolt": False}

    def test_extract(self, session):
        extract_youtube_videos(self.channels, **self.dk)
        assert session.query(Channel).count() == 1
        assert session.query(Video).count() == 1

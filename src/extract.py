import json
import threading
from datetime import datetime
from typing import Sequence

import youtube_dl
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError, OperationalError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from . import BASE_DIR
from .models import Base, Channel, Video


DEF_DB_URI = "mysql+mysqlconnector://root@127.0.0.1:3306/words_in_political_media"


def save_as_json(path, data: dict):
    with path.open("w") as fp:
        # Don't use path.write_text since converting to text no-good for mem
        json.dump(data, fp)


def extract_youtube_videos(channels: Sequence, **kwargs):
    def download_task(url):
        with youtube_dl.YoutubeDL({"ignoreerrors": True}) as ydl:
            data = ydl.extract_info(url, download=False)
        if data is None:
            raise ValueError("Couldn't download data from YouTube.")
        channel = data["uploader_id"]
        path = BASE_DIR / "data" / "youtube" / f"{channel}.json"
        if kwargs.get("save_as_json") and (
            (path.is_file() and not kwargs.get("do_not_overwrite"))
            or not path.is_file()
        ):
            save_as_json(path, data)
        if kwargs.get("save_in_dolt"):
            dolt = SaveItDolt(data, kwargs.get("db_uri"), kwargs)
            with dolt:
                dolt.save_videos(use_ch_entry=False)

    if not kwargs.get("threaded"):
        [download_task(p) for p in channels]
        return
    # Output from multiple threads still works in one console
    threads = [threading.Thread(target=download_task, args=(p,)) for p in channels]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


class SaveItDolt:
    """Interface for saving records in Dolt with our specified methodology"""

    channel: Channel = None

    def __init__(
        self,
        data: dict = None,
        db_uri=DEF_DB_URI,
        main_kwargs=None,
        *,
        setup_dolt=True,
    ):
        self.data = data
        if not main_kwargs:
            main_kwargs = {}
        self.kwargs = main_kwargs
        self._db_uri = db_uri
        self._setup_dolt: bool = setup_dolt

    def __enter__(self):
        self.engine = create_engine(self._db_uri or DEF_DB_URI)
        self.Session = scoped_session(sessionmaker(self.engine))
        if self._setup_dolt or self.kwargs.get("setup_dolt"):
            self.setup_dolt()

    def __exit__(self, *args, **kwargs):
        self.engine.dispose()

    def setup_dolt(self):
        try:
            Base.metadata.create_all(self.engine, checkfirst=True)
        except (DatabaseError, OperationalError) as e:
            print("Database/Operational Error:", e)
            channel = self.data["uploader_id"]
            path = BASE_DIR / "data" / "youtube" / f"{channel}.json"
            if not self.kwargs.get("save_as_json"):
                if self.kwargs.get("threaded"):
                    print("Saving as JSON due to database error for backup purposes.")
                    save_as_json(path, self.data)
                else:
                    response = input("Do you want to save as JSON as backup? [Y/n]: ")
                    if (response.lower() or "y") == "y":
                        save_as_json(path, self.data)
            print(
                "Exiting program due to no connection to Dolt DB. "
                "Please setup your Dolt database first or do not specify "
                "that you would like to save in Dolt."
            )
            quit(1)

    # DB Interface
    # --------------------------------------------------
    def get_or_save_channel(self) -> Channel:
        """Returns channel ID. If channel does not exist, create first."""
        print(f"Getting Existing/Saving new channel: {self.data['uploader']}")
        session = self.Session()
        try:
            self.channel = (
                session.query(Channel)
                .filter_by(uploader_id=self.data["uploader_id"])
                .one()
            )
        except NoResultFound:
            self.channel = Channel(
                name=self.data["uploader"],
                uploader_id=self.data["uploader_id"],
                playlist_id=self.data["id"],
            )
            session.add(self.channel)
            session.commit()
        return self.channel

    def save_videos(self, *, use_ch_entry: bool = False):
        """
        :param use_ch_entry: uses the channel ID from the entry. You should DEFINITELY
        run get_or_save_channel() instead so that we don't have bad FKs.
        :return: list of videos
        """
        if not self.channel and not use_ch_entry:
            self.get_or_save_channel()

        def create_video_kwargs(_entry: dict):
            # Many DB attributes are the same as the API returns
            keys = ("title", "view_count", "dislike_count")
            return {key: _entry[key] for key in keys}

        print(f"Saving/updating videos for: {self.data['uploader']}")
        session = self.Session()
        for data in self.data["entries"]:
            try:
                old_vid = session.query(Video).filter_by(video_id=data["id"]).one()
                for x in Video.updatable_attributes():
                    setattr(old_vid, x, data[x])
                session.add(old_vid)
            except NoResultFound:
                session.add(
                    Video(
                        video_id=data["id"],
                        upload_date=datetime.strptime(data["upload_date"], "%Y%m%d"),
                        channel_id=data["uploader_id"]
                        if use_ch_entry
                        else self.channel.id,
                        **create_video_kwargs(data),
                    )
                )
            except Exception as e:
                # Possibly due to privatized video
                print(f"Code Error: {e}")
        session.commit()

    @classmethod
    def save_json_in_dolt(cls, json_path: str):
        """
        Convenience method to save data in Dolt after failed attempt at saving
        during main program. This is meant for scripting in a console.
        """
        with open(json_path) as fp:
            data = json.load(fp)
        dope = cls(data)
        dope.save_videos(use_ch_entry=False)

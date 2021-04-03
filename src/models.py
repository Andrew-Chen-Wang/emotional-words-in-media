from datetime import datetime

from pytz import utc
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def utcnow():
    return datetime.utcnow().replace(tzinfo=utc)


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(200))
    uploader_id = Column(String(200), unique=True, index=True)
    playlist_id = Column(String(200))


class SLBigInteger(BigInteger):
    pass


@compiles(SLBigInteger, "sqlite")
def bi_c(_element, _compiler, **_kw):
    return "INTEGER"


@compiles(SLBigInteger)
def bi_c(element, compiler, **kw):
    return compiler.visit_BIGINT(element, **kw)


class Video(Base):
    __tablename__ = "video"

    # Meta
    id = Column(SLBigInteger, autoincrement=True, primary_key=True)
    record_created = Column(DateTime, default=utcnow)
    # Video
    video_id = Column(String(60), unique=True, index=True)
    title = Column(String(255))
    # Because we use dolt, we'll know when an attribute is changed.
    # I wanted a JSON type but didn't want a separate table with an FK to here
    # just for a changelog. Maybe if someone takes maintainership they can do it
    view_count = Column(BigInteger)
    like_count = Column(BigInteger)
    dislike_count = Column(BigInteger)
    upload_date = Column(Date)
    last_known_privatized = Column(Date, nullable=True)
    channel_id = Column(Integer, ForeignKey("channel.id"))

    @classmethod
    def updatable_attributes(cls, include_privatized=False):
        return [
            "title",
            "view_count",
            "like_count",
            "dislike_count",
        ] + (["last_known_privatized"] if include_privatized else [])

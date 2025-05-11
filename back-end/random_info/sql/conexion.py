from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Genre(Base):
    __tablename__ = 'genre_spotify'
    id = Column(Integer, primary_key=True)
    names = Column(String, unique=True, nullable=False)


Base = declarative_base()


class Band(Base):
    __tablename__ = "band_spotify"
    id = Column(Integer, primary_key=True)
    id_spotify = Column(String(30), unique=True, nullable=False)
    names = Column(String(100), nullable=False)
    names_normalize = Column(String(100), nullable=False)
    img_url = Column(String(255))
    popularity = Column(Integer)
    date_create = Column(TIMESTAMP, server_default=func.current_timestamp())
    date_up = Column(TIMESTAMP, server_default=func.current_timestamp(
    ), onupdate=func.current_timestamp())

    def __init__(self, id_spotify: str, names: str, names_normalize: str, img_url: str, popularity=0):
        self.id_spotify = id_spotify
        self.names = names
        self.names_normalize = names_normalize
        self.img_url = img_url
        self.popularity = popularity


class BandGenre(Base):
    __tablename__ = "band_genre_spotify"
    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey(
        "band_spotify.id", ondelete="CASCADE"), nullable=False)
    genre_id = Column(Integer, ForeignKey(
        "genre_spotify.id", ondelete="CASCADE"), nullable=False)

    # Clave única para evitar duplicaciones
    __table_args__ = (UniqueConstraint(
        'band_id', 'genre_id', name='band_genre_unique'),)

    def __init__(self, band_id, genre_id):
        self.band_id = band_id
        self.genre_id = genre_id

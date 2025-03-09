from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# Inicializar SQLAlchemy
db = SQLAlchemy()


# Clase para la tabla "band"
class Band(db.Model):
    __tablename__ = "band_spotify"
    id = db.Column(db.Integer, primary_key=True)
    id_spotify = db.Column(db.String(30), unique=True, nullable=False)
    names = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(255))
    popularidad = db.Column(db.Integer)
    date_create = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_up = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def __init__(self, id_spotify: str, names: str, img_url: str):
        self.id_spotify = id_spotify
        self.names = names
        self.img_url = img_url

# Definir el modelo de la tabla "genre"


class Genre(db.Model):
    __tablename__ = "genre_spotify"
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, names: str):
        self.names = names

# Definir el modelo de la tabla intermedia "band_genre"


class BandGenre(db.Model):
    __tablename__ = "band_genre_spotify"
    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey(
        "band_spotify.id", ondelete="CASCADE"), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey(
        "genre_spotify.id", ondelete="CASCADE"), nullable=False)

    # Clave única para evitar duplicaciones
    __table_args__ = (db.UniqueConstraint(
        'band_id', 'genre_id', name='band_genre_unique'),)

    def __init__(self, band_id, genre_id):
        self.band_id = band_id
        self.genre_id = genre_id

# Función para buscar una banda por su nombre


def search_band_db(name_query):
    if not name_query:
        return {"error": "El parámetro 'name_query' es obligatorio"}, 400

    try:
        # Consulta optimizada con filtro LIKE
        bands = Band.query.filter(func.lower(
            Band.names).contains(func.lower(name_query))).all()

        if not bands:
            return {"message": "No se encontraron bandas"}, 404

        result = []
        for band in bands:
            # Obtener los géneros asociados a esta banda
            genres_query = db.session.query(Genre).join(
                BandGenre).filter(BandGenre.band_id == band.id).all()  # type: ignore
            genres = [genre.names for genre in genres_query]

            # Crear el objeto de banda con el formato deseado
            band_obj = {
                "id": band.id,
                "band_id": band.id_spotify,  # id_spotify en tu BD es band_id en tu formato
                "name": band.names,
                "img": band.img_url,
                "genres": genres,
                "popularity": band.popularidad,
                "date_create": band.date_create,
                "date_up": band.date_up
            }
            result.append(band_obj)

        return result
    except Exception as e:
        return {"error": f"Error al buscar bandas: {str(e)}"}, 500
# Función para agregar una banda y asociar géneros


def add_band(band_data):
    if not band_data or not all(key in band_data for key in ["id", "name", "img", "genres"]):
        return {"error": "Datos incompletos. Se requieren 'id', 'name', 'img' y 'genres'."}, 400

    # Verificar si la banda ya existe en la base de datos
    existing_band = Band.query.filter_by(id_spotify=band_data["id"]).first()
    if existing_band:
        return {"message": "La banda ya existe", "id": existing_band.id}, 409

    # Crear la nueva banda
    new_band = Band(
        id_spotify=band_data["id"],
        names=band_data["name"],
        img_url=band_data["img"]
    )
    db.session.add(new_band)
    db.session.commit()  # Confirmar la creación para obtener el ID

    # Manejo de géneros y relaciones
    genre_ids = []
    for genre_name in band_data["genres"]:
        # Verificar si el género ya existe
        genre = Genre.query.filter(func.lower(
            Genre.names) == func.lower(genre_name)).first()
        # Si no existe, crearlo
        if not genre:
            genre = Genre(names=genre_name)
            db.session.add(genre)
            db.session.commit()  # Confirmar el nuevo género para obtener su ID

        # Asociar género con la banda
        band_genre = BandGenre(band_id=new_band.id, genre_id=genre.id)
        db.session.add(band_genre)
        genre_ids.append(genre.id)

    db.session.commit()  # Confirmar todas las relaciones

    return {
        "message": "Banda agregada correctamente",
        "band_id": new_band.id,
        "genres": genre_ids
    }, 201

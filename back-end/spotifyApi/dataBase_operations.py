from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import scoped_session, sessionmaker

from services.compare_dictstring import find_bands_dict_array

# Inicializar SQLAlchemy
db = SQLAlchemy()


def create_session():
    return scoped_session(sessionmaker(bind=db.engine))


# Clase para la tabla "band"
class Band(db.Model):
    __tablename__ = "band_spotify"
    id = db.Column(db.Integer, primary_key=True)
    id_spotify = db.Column(db.String(30), unique=True, nullable=False)
    names = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(255))
    popularity = db.Column(db.Integer)
    date_create = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_up = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def __init__(self, id_spotify: str, names: str, img_url: str, popularity=0):
        self.id_spotify = id_spotify
        self.names = names
        self.img_url = img_url
        self.popularity = popularity

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
                "popularity": band.popularity,
                "date_create": band.date_create,
                "date_up": band.date_up
            }
            result.append(band_obj)

        return result
    except Exception as e:
        return {"error": f"Error al buscar bandas: {str(e)}"}, 500
# Función para agregar una banda y asociar géneros


def search_bands_db_from_list(bands_list):
    if not bands_list or not isinstance(bands_list, list):
        return {"error": "La entrada debe ser una lista de bandas"}, 400

    result = []

    # Extraer los nombres de las bandas de la lista
    band_names = [band["name"] for band in bands_list]
    # valido que sea una lista de str
    if not all(isinstance(name, str) for name in band_names):
        return {"error": "El nombre de las bandas debe ser un string"}, 400
    # Creo una consula SQL a la columna names para obtener todas las bandas que estan en la lista band_names
    bands_query = Band.query.filter(
        Band.names.in_(band_names)).all()  # type: ignore

    # imprimo el largo de la lista de bandas
    print('bands_query len ->', len(bands_query))
    print('bands_list len ->', len(bands_list))

    # Comparo los array y obtengo los entonctrados y los no encontrados
    bands_found, bands_not_found = find_bands_dict_array(
        band_names, bands_query)
    # bands_found => <Band> object
    # bands_not_found => <str> object

    # Si no encontramos bandas, retornamos temprano
    if not len(bands_found) > 0:
        return [], bands_not_found

    # Obtenemos los IDs de las bandas encontradas para consultar los géneros
    band_ids = [band.id for band in bands_found]

    # --- obtengo los generos de las bandas encontradas ---
    # Hago una sola consulta para obtener todos los genre_id de los bands_ids
    band_genres_query = BandGenre.query.filter(
        BandGenre.band_id.in_(band_ids)).all()  # type: ignore

    # Ahora obtenemos todos los géneros necesarios
    genre_ids = [bg.genre_id for bg in band_genres_query]
    genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()

    # Crear un diccionario para mapear genre_id a nombre de género
    genre_dict = {genre.id: genre.names for genre in genres}
    # Organizar los géneros por band_id
    band_genres = {}
    for bg in band_genres_query:
        if bg.band_id not in band_genres:
            band_genres[bg.band_id] = []
        # Añadir el nombre del género usando nuestro diccionario
        if bg.genre_id in genre_dict:
            band_genres[bg.band_id].append(genre_dict[bg.genre_id])

    # --- obtengo los generos de las bandas encontradas ---
    # Convertimos bands_found (lista de objetos Band) a un diccionario para búsqueda eficiente
    bands_found_dict = {}
    for band in bands_found:
        # Usando minúsculas para case-insensitive
        bands_found_dict[band.names.lower()] = band

    # Ahora iteramos sobre bands_list y actualizamos con la información
    for band in bands_list:
        # Convertimos a minúsculas para la comparación
        band_name = band["name"].lower()

        if band_name in bands_found_dict:
            found_band = bands_found_dict[band_name]
            band["band_id"] = found_band.id_spotify
            band["popularity"] = found_band.popularity
            band["img_url"] = found_band.img_url
            # Ahora agregamos la información de géneros
            band["genres"] = band_genres.get(found_band.id, [])

            result.append(band)
        else:
            # Buscamos en bands_not_found
            for not_found_band in bands_not_found:
                if 'name' in not_found_band and not_found_band['name'].lower() == band_name:
                    # Añadimos información de img_zone a la banda no encontrada
                    not_found_band['img_zone'] = band.get('img_zone', [])
                    break

    print('bands_list result ->', len(result))
    print('bands_not_found ->', len(bands_not_found))
    return result, bands_not_found


def add_band(band_data):
    if not band_data or not all(key in band_data for key in ["id", "name", "img", "genres"]):
        return {"error": "Datos incompletos. Se requieren 'id', 'name', 'img' y 'genres'."}, 400

    # Crear una nueva sesión para esta operación
    session = create_session()

    try:
        # Verificar si la banda ya existe en la base de datos
        existing_band = session.query(Band).filter_by(
            id_spotify=band_data["id"]).first()
        if existing_band:
            return {"message": "La banda ya existe", "id": existing_band.id}, 409

        # Crear la nueva banda
        new_band = Band(
            id_spotify=band_data["id"],
            names=band_data["name"],
            img_url=band_data["img"],
            # Usar .get para manejar casos donde no exista
            popularity=band_data.get("popularity", 0)
        )
        session.add(new_band)
        session.commit()  # Confirmar la creación para obtener el ID

        # Manejo de géneros y relaciones
        genre_ids = []
        for genre_name in band_data["genres"]:
            # Verificar si el género ya existe
            genre = session.query(Genre).filter(func.lower(
                Genre.names) == func.lower(genre_name)).first()
            # Si no existe, crearlo
            if not genre:
                genre = Genre(names=genre_name)
                session.add(genre)
                session.commit()  # Confirmar el nuevo género para obtener su ID

            # Asociar género con la banda
            band_genre = BandGenre(band_id=new_band.id, genre_id=genre.id)
            session.add(band_genre)
            genre_ids.append(genre.id)

        session.commit()  # Confirmar todas las relaciones

        return {
            "message": "Banda agregada correctamente",
            "band_id": new_band.id,
            "genres": genre_ids
        }, 201

    except Exception as e:
        session.rollback()
        return {"error": f"Error al agregar banda: {str(e)}"}, 500

    finally:
        session.close()

from dao.model.genre import GenreSchema


genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


class GenreService:
    def __init__(self, genre_dao):
        self.genre_dao = genre_dao

    def get_all(self):
        """Возвращает список всех жанров"""
        genres = self.genre_dao.get_all()

        return genres_schema.dump(genres)

    def create(self, data):
        """Создает жанр"""
        genre = self.genre_dao.create(data)

        return genre_schema.dump(genre)

    def get_one(self, gid):
        """Возвращает 1 жанр по id"""
        genre = self.genre_dao.get_one(gid)

        return genre_schema.dump(genre)

    def update(self, data):
        """Обновляет жанр по id и всем полям таблицы"""
        gid = data.get('id')

        genre = self.genre_dao.get_one(gid)

        if not genre:
            return None

        genre.name = data.get("name")

        genre = self.genre_dao.update(genre)

        return genre_schema.dump(genre)

    def delete(self, gid):
        """Удаляет жанр по id"""
        genre = self.genre_dao.get_one(gid)

        if not genre:
            return None

        self.genre_dao.delete(genre)

        return genre_schema.dump(genre)

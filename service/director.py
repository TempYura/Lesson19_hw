from dao.model.director import DirectorSchema


director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


class DirectorService:
    def __init__(self, director_dao):
        self.director_dao = director_dao

    def get_all(self):
        """Возвращает список всех режиссеров"""
        directors = self.director_dao.get_all()

        return directors_schema.dump(directors)

    def create(self, data):
        """Создает режиссера"""
        director = self.director_dao.create(data)

        return director_schema.dump(director)

    def get_one(self, gid):
        """Возвращает 1 режиссера по id"""
        director = self.director_dao.get_one(gid)

        return director_schema.dump(director)

    def update(self, data):
        """Обновляет режиссера по id и всем полям таблицы"""
        gid = data.get('id')

        director = self.director_dao.get_one(gid)

        if not director:
            return None

        director.name = data.get("name")

        director = self.director_dao.update(director)

        return director_schema.dump(director)

    def delete(self, gid):
        """Удаляет режиссера по id"""
        director = self.director_dao.get_one(gid)

        if not director:
            return None

        self.director_dao.delete(director)

        return director_schema.dump(director)

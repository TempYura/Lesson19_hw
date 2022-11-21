from flask import request
from flask_restx import Resource, Namespace
from container import genre_service
from deccorators import auth_required, admin_required

genres_ns = Namespace("genres")


@genres_ns.route("/")
class GenresView(Resource):
    @auth_required
    def get(self):
        """
        Возвращает список всех жанров
        """
        genres = genre_service.get_all()

        if not genres:
            return "Не найдено", 404

        return genres, 200

    @admin_required
    def post(self):
        """Добавляет жанр"""
        req_json = request.json

        genre = genre_service.create(req_json)

        return genre, 201,  {"location": f"/{genres_ns.name}/{genre['id']}"}


@genres_ns.route("/<int:gid>")
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        """Возвращает подробную информацию о жанре"""
        genre = genre_service.get_one(gid)

        if not genre:
            return "Не найдено", 404

        return genre, 200

    @admin_required
    def put(self, gid):
        """Обновляет жанр"""
        req_json = request.json
        req_json["id"] = gid

        genre = genre_service.update(req_json)

        if not genre:
            return "Не найдено", 404

        return genre, 200

    @admin_required
    def delete(self, gid):
        """Удаляет жанр"""
        genre = genre_service.delete(gid)

        if not genre:
            return "Не найдено", 404

        return genre, 200

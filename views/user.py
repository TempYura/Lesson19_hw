from flask import request
from flask_restx import Resource, Namespace
from container import user_service


users_ns = Namespace("users")


@users_ns.route("/")
class UsersView(Resource):
    def get(self):
        """
        Возвращает список всех пользователей.
        Можно фильтровать по role
        """
        args = request.args.to_dict()

        users = user_service.get_all(args)

        if not users:
            return "Не найдено", 404

        return users, 200

    def post(self):
        """Добавляет пользователя"""
        req_json = request.json

        user = user_service.create(req_json)

        return user, 201,  {"location": f"/{users_ns.name}/{user['id']}"}


@users_ns.route("/<int:uid>")
class UserView(Resource):
    def get(self, uid):
        """Возвращает подробную информацию о пользователе по id"""
        user = user_service.get_one(uid)

        if not user:
            return "Не найдено", 404

        return user, 200

    def put(self, uid):
        """Обновляет пользователя"""
        req_json = request.json
        req_json["id"] = uid

        user = user_service.update(req_json)

        if not user:
            return "Не найдено", 404

        return user, 200

    def delete(self, uid):
        """Удаляет пользователя"""
        user = user_service.delete(uid)

        if not user:
            return "Не найдено", 404

        return user, 200

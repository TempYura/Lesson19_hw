from flask import request, abort
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

        username = req_json.get("username")
        password = req_json.get("password")
        role = req_json.get("role", "user")

        if None in [username, password]:
            abort(400)

        user_in_db = user_service.get_by_username(username)

        if user_in_db:
            return "Пользователь с таким именем уже существует, для обновления используйте метод put", 404

        password_hash = user_service.get_hash(password)

        data = {
            "username": username,
            "password": password_hash,
            "role": role
        }

        user = user_service.create(data)


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

        username = req_json.get("username")
        password = req_json.get("password")
        role = req_json.get("role")

        if None in [username, password, role]:
            abort(404)

        password_hash = user_service.get_hash(password)

        data = {
            "username": username,
            "password": password_hash,
            "role": role
        }

        user = user_service.update(data)

        if not user:
            return "Не найдено", 404

        return user, 200

    def delete(self, uid):
        """Удаляет пользователя"""
        user = user_service.delete(uid)

        if not user:
            return "Не найдено", 404

        return user, 200

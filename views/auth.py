import calendar
import datetime

import jwt as jwt
from flask import request, abort
from flask_restx import Resource, Namespace
from container import user_service, auth_service
from constants import JWT_ALGO, JWT_SECRET


auth_ns = Namespace("auth")


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        """получает логин и пароль из Body запроса в виде JSON,
        далее проверяет соотвествие с данными в БД
        (есть ли такой пользователь, такой ли у него пароль)
        и если всё оk — генерит пару access_token и refresh_token и
        отдает их в виде JSON."""
        req_json = request.json

        username = req_json.get("username")
        password = req_json.get("password")

        # if not all(username, password):
        #     return abort(400)
        #
        # user = user_service.get_one(username)
        #
        # if not user:
        #     return abort(404)
        #
        # if user_service.get_hash(password) != user.get("password"):
        #     return abort(400)
        #
        #
        # data = {
        #     "username": user.username,
        #     "role": user.role
        # }
        #
        # min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        # data["exp"] = calendar.timegm(min30.timetuple())
        # access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)
        #
        # days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        # data["exp"] = calendar.timegm(days130.timetuple())
        # refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)
        #
        # tokens = {"access_token": access_token, "refresh_token": refresh_token}
        tokens = auth_service.generate_token(username, password)

        return tokens, 201

    def put(self):
        """получает refresh_token из Body запроса в виде JSON,
        далее проверяет refresh_token и если он не истек и валиден —
        генерит пару access_token и refresh_token и
        отдает их в виде JSON."""

        req_json = request.json
        refresh_token = req_json.get("refresh_token")

        # if not refresh_token:
        #     return abort(400)
        #
        # try:
        #     data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGO])
        # except Exception as e:
        #     abort(400)
        #
        # username = data.get("username")
        #
        # user = user_service.get_one(username)
        #
        # data = {
        #     "username": user.username,
        #     "role": user.role
        # }
        #
        # min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        # data["exp"] = calendar.timegm(min30.timetuple())
        # access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)
        #
        # days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        # data["exp"] = calendar.timegm(days130.timetuple())
        # refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)
        #
        # tokens = {"access_token": access_token, "refresh_token": refresh_token}

        tokens = auth_service.check_token(refresh_token)

        return tokens, 201


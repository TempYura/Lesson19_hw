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

        if None in [username, password]:
            abort(401)

        tokens = auth_service.generate_token(username, password)

        return tokens, 201

    def put(self):
        """получает refresh_token из Body запроса в виде JSON,
        далее проверяет refresh_token и если он не истек и валиден —
        генерит пару access_token и refresh_token и
        отдает их в виде JSON."""

        req_json = request.json
        refresh_token = req_json.get("refresh_token")

        tokens = auth_service.check_token(refresh_token)

        return tokens, 201


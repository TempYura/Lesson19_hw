import base64
import hashlib
import hmac

from dao.model.user import UserSchema
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def get_all(self, args):
        """Возвращает всех пользователей.
        Фильтрует результаты средствами sql, если были заданы фильтры.
        """
        if not args:
            users = self.user_dao.get_all()
            return users_schema.dump(users)


        allowed_filter_list = ["role"]

        filter_list = []

        for arg in args:
            if arg in allowed_filter_list:
                filter_list.append(f"{arg} = {args.get(arg)}")
            else:
                return None

        filter = ' AND '.join(filter_list)

        users = users_schema.dump(self.user_dao.get_filtered(filter))

        return users

    def create(self, data):
        """Добавляет пользователя"""
        user = self.user_dao.create(data)

        return user_schema.dump(user)

    def get_one(self, uid):
        """Возвращает 1 пользователя по id"""
        user = self.user_dao.get_one(uid)

        return user_schema.dump(user)

    def get_by_username(self, username):
        user = self.user_dao.get_by_username(username)

        return user_schema.dump(user)

    def update(self, data):
        """Обновляет пользователя по id и всем полям таблицы"""
        uid = data.get('id')

        user = self.user_dao.get_one(uid)

        if not user:
            return None

        user.username = data.get("username")
        user.role = data.get("role")

        return user_schema.dump(self.user_dao.update(user))

    def delete(self, uid):
        """Удаляет пользователя по id"""
        user = self.user_dao.get_one(uid)

        if not user:
            return None

        self.user_dao.delete(user)

        return user_schema.dump(user)

    def get_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

        # return hashlib.pbkdf2_hmac(
        #     'sha256',
        #     password.encode('utf-8'),  # Convert the password to bytes
        #     PWD_HASH_SALT,
        #     PWD_HASH_ITERATIONS
        # ).decode("utf-8", "ignore")

    def compare_passwords(self, password_hash, request_password):
        return hmac.compare_digest(
            base64.b16decode(password_hash),
            hashlib.pbkdf2_hmac('sha256',
                                request_password.encode('utf-8'),  # Convert the password to bytes
                                PWD_HASH_SALT,
                                PWD_HASH_ITERATIONS
                                )
        )
from dao.sqlite_dao import DAO
from dao.model.movie import Movie


class MovieDAO(DAO):
    def __init__(self, session):
        self.session = session
        self.model = Movie

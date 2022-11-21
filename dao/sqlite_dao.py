from sqlalchemy import text


class DAO:
    def __init__(self, session, model):
        self.session = session
        self.model = model

    def get_one(self, oid):
        m_object = self.session.query(self.model).get(oid)
        return m_object

    def get_all(self):
        m_objects = self.session.query(self.model).all()
        return m_objects

    def get_filtered(self, text_filter):
        m_objects = self.session.query(self.model).filter(text(text_filter)).all()
        return m_objects

    def update(self, m_object):
        self.session.add(m_object)
        self.session.commit()

        return m_object

    def delete(self, m_object):
        self.session.delete(m_object)
        self.session.commit()

        return m_object

    def create(self, data):
        m_object = self.model(**data)

        self.session.add(m_object)
        self.session.commit()

        return m_object

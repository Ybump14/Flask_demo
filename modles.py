## -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def sql_connect():
    engine = create_engine("mysql://root:root@localhost:3306/test?charset=utf8", encoding='utf-8')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)
    return session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    loginnum = Column(String(255))
    password = Column(String(255))

    def __repr__(self):
        return "<User(id='%s', loginnum='%s',password='%s')>" % (
            self.id, self.loginnum, self.password)


db = sql_connect()
db_add = User(loginnum="a123",password="123")
db.add(db_add)
db.commit()
db.close()

db_user = db.query(User).filter().all()
db.delete(db_user)
db.commit()

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('shul_id', Integer, ForeignKey('shuls.id')),
    # ENUM for association type (gabbai, leiner)
)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    name = Column(String(100))
    shul = relationship(
        'Shuls',
        secondary=association_table,
        back_populates='user'
    )


class Shuls(Base):
    __tablename__ ='shuls'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    address = Column(String(200))
    city = Column(String(25))
    state = Column(String(2))
    zip = Column(String(10))
    calendar_type = Column(String(8))
    shabbos_signup = Column(Boolean, default=True)
    yomtov_signup = Column(Boolean, default=False)
    visibility = Column(String(10))
    accessibility = Column(String(10))
    user = relationship(
        'Users',
        secondary=association_table,
        back_populates='shul'
    )
    weeks = relationship('Weeks')


class Weeks(Base):
    __tablename__ = 'weeks'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    shul_id = Column(Integer, ForeignKey('shuls.id'))
    parasha = Column(String(50))
    full = Column(Integer, ForeignKey('users.id'), nullable=True)
    rishon = Column(Integer, ForeignKey('users.id'), nullable=True)
    sheini = Column(Integer, ForeignKey('users.id'), nullable=True)
    shelishi = Column(Integer, ForeignKey('users.id'), nullable=True)
    revii = Column(Integer, ForeignKey('users.id'), nullable=True)
    chamishi = Column(Integer, ForeignKey('users.id'), nullable=True)
    shishi = Column(Integer, ForeignKey('users.id'), nullable=True)
    shevii = Column(Integer, ForeignKey('users.id'), nullable=True)
    maftir = Column(Integer, ForeignKey('users.id'), nullable=True)
    haftarah = Column(Integer, ForeignKey('users.id'), nullable=True)


engine = create_engine('sqlite:///leining.db')
Base.metadata.create_all(engine)

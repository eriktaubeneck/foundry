from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship


def models_factory(Base):
    class Crew(Base):
        __tablename__ = 'crew'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        birthday = Column(DateTime)
        role = Column(String)
        salary = Column(Numeric(12, 2))
        ship_id = Column(String, ForeignKey('ship.id'))
        planet_id = Column(String, ForeignKey('planet.id'))

    class Ship(Base):
        __tablename__ = 'ship'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        call_sign = Column(String)
        purchased_at = Column(DateTime)
        warranty_expires_at = Column(DateTime)
        last_serviced_at = Column(DateTime)
        crew = relationship('Crew', backref='ship', lazy='dynamic')

    class Planet(Base):
        __tablename__ = 'planet'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        residents = relationship('Crew', backref='planet', lazy='dynamic')

    return Crew, Ship, Planet

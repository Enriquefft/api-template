"""Module for database models and session creation."""

from sqlalchemy import Column, Integer, MetaData, String, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

from env import PG_DATABASE, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER, PROJECT_NAME

db_url = URL.create(
    drivername="postgresql",
    username=PG_USER,
    password=PG_PASSWORD,
    host=PG_HOST,
    database=PG_DATABASE,
    port=PG_PORT,
)


# https://community.render.com/t/solved-psycopg2-operationalerror-ssl-connection-has-been-closed-unexpectedly/14462
engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(bind=engine)


Base = declarative_base(metadata=MetaData(schema=PROJECT_NAME))


class User(Base):
    """Model for user table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    name = Column(String)


Base.metadata.create_all(engine)

from contextlib import _GeneratorContextManager, contextmanager
import functools
from typing import Any, Callable, Concatenate, Generator, ParamSpec, TypeVar
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, orm, Engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.sql import text
from sqlalchemy_utils.functions import database_exists, create_database
import logging

Base = declarative_base()

TDatabaseFactory = Callable[[], _GeneratorContextManager[Session]]


class Database:
    def __init__(self, db_host: str, db_port: int, db_user: str, db_password: str, db_name: str) -> None:
        self.__engine_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.__engine = create_engine(self.__engine_url, echo=True)
        self.__session_factory = orm.scoped_session(
            orm.sessionmaker(bind=self.__engine, autoflush=True, expire_on_commit=True, autocommit=False, future=True)
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.create_db()

    @property
    def session_factory(self) -> scoped_session[Session]:
        return self.__session_factory

    def create_db(self) -> None:
        if not database_exists(self.__engine.url):
            create_database(self.__engine.url)
            self.logger.info(f"Created database {self.__engine.url}")
        else:
            self.logger.info(f"Database {self.__engine.url} already exists")

    def simple_session(self) -> Session:
        session: Session = self.__session_factory()
        try:
            return session
        except Exception as e:
            self.logger.exception("Session rollback because of exception")
            session.rollback()
            raise e
        finally:
            session.close()

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session: Session = self.__session_factory()
        try:
            yield session
        except Exception as e:
            self.logger.exception("Session rollback because of exception")
            session.rollback()
            raise e
        finally:
            session.close()

    def ping(self) -> bool:
        try:
            with self.session() as session:
                session.execute(text("SELECT 1"))
                return True
        except Exception as e:
            self.logger.exception(f"Failed to ping database with error: {e}")
            return False

    @property
    def url(self) -> str:
        return self.__engine_url

    @property
    def base(self) -> Any:
        return Base

    @property
    def engine(self) -> Engine:
        return self.__engine

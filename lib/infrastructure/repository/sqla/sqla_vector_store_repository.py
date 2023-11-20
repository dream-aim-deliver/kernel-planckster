from sqlalchemy.orm.session import Session

from lib.core.ports.secondary.vector_store_repository import VectorStoreRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory


class SQLAVectorStoreRepository(VectorStoreRepositoryOutputPort):
    def __init__(self, session_factory: TDatabaseFactory) -> None:
        super().__init__()
        with session_factory() as session:
            self._session = session

    @property
    def session(self) -> Session:
        return self._session

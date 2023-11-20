from lib.core.entity.models import VectorStore
from lib.core.sdk.dto import BaseDTO


class NewVectorStoreDTO(BaseDTO[VectorStore]):
    """
    DTO for the new vector store use case.

    @param vector_store_id: The vector store that was created.
    @type vector_store_id: int | None = None
    """

    vector_store_id: int | None = None

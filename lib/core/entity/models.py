from enum import Enum
from pydantic import BaseModel
from typing import TypeVar
from datetime import datetime


class ProtocolEnum(Enum):
    """
    Enum for the different protocols that can be used to store a source_data.
    """

    S3 = "s3"
    NAS = "nas"
    LOCAL = "local"


class BaseKernelPlancksterModel(BaseModel):
    """
    Base class for all models in the project

    @param created_at: the datetime when the model was created
    @param updated_at: the datetime when the model was last updated
    """

    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        return f"created_at: {self.created_at}, updated_at: {self.updated_at}"


class BaseSoftDeleteKernelPlancksterModel(BaseKernelPlancksterModel):
    """
    Base class for all models in the project that can be soft deleted

    @param deleted: whether the model is deleted or not
    @param deleted_at: the datetime when the model was deleted
    """

    deleted: bool
    deleted_at: datetime | None

    def __str__(self) -> str:
        return super().__str__() + f", deleted: {self.deleted}, deleted_at: {self.deleted_at}"


class User(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a user in the system

    @param id: the id of the user
    @type id: int
    @param sid: the sid of the user
    @type sid: str
    """

    id: int
    sid: str

    def __str__(self) -> str:
        return "User: " + super().__str__() + f", id: {self.id}, sid: {self.sid}"


class KnowledgeSource(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a knowledge source, a collection of sources defined by the user

    @param id: the id of the knowledge source
    @param source: the source of the source_data (e.g., Google, YouTube, UserUpload, etc.)
    @param content_metadata: depending on the source, can be the query made to the source or the list of user uploads; meant to be a json formatted string, including e.g. an URL
    """

    id: int
    source: str
    content_metadata: str

    def __str__(self) -> str:
        return (
            "KnowledgeSource: "
            + super().__str__()
            + f", id: {self.id}, source: {self.source}, content_metadata: {self.content_metadata}"
        )


class SourceData(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a source_data or a file

    @param id: the id of the source_data
    @param name: the name of the source_data
    @param type: the type of the source_data (e.g., pdf, txt, etc.)
    @param lfn: the logical file name of the source_data
    @param protocol: the protocol used to store the source_data
    """

    id: int
    name: str
    type: str
    lfn: str
    protocol: ProtocolEnum

    def __str__(self) -> str:
        return (
            "SourceData: "
            + super().__str__()
            + f", id: {self.id}, name: {self.name}, lfn: {self.lfn}, protocol: {self.protocol}"
        )


class EmbeddingModel(BaseSoftDeleteKernelPlancksterModel):
    """
    An embedding model is a model that can be used to embed a vector storde associated with a research context (including its source data), into a vector space

    @param id: the id of the embedding model
    @param name: the name of the embedding model
    """

    id: int
    name: str


class LLM(BaseSoftDeleteKernelPlancksterModel):
    """
    A LLM (Language Learning Model) is a model that can be used to generate a response to a user query, given a vectorized research context

    @param id: the id of the LLM
    @param name: the name of the LLM
    """

    id: int
    llm_name: str


class ResearchContext(BaseSoftDeleteKernelPlancksterModel):
    """
    A research context belongs to a research topic, and is defined using a subset of the collection of source_data of the research topic
    This is the context in which conversations will happen

    @param id: the id of the research context
    @param title: the title of the research context
    """

    id: int
    title: str


class VectorStore(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a vector store, a vectorization of a research context to be inputted to an LLM

    @param id: the id of the vector store
    @param name: the name of the vector store
    @param lfn: the logical file name of the vector store
    @param protocol: the protocol used to store the vector store
    """

    id: int
    name: str
    lfn: str
    protocol: ProtocolEnum


class Conversation(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a conversation between a user and an agent, within in a research context
    This is where messages will be exchanged

    @param id: the id of the conversation
    @param title: the title of the conversation
    """

    id: int
    title: str


class MessageBase(BaseSoftDeleteKernelPlancksterModel):
    """
    Base class for user queries and agent responses

    @param id: the id of the message
    @param content: the content of the message
    @param timestamp: the datetime when the message was sent
    """

    id: int
    content: str
    timestamp: datetime


TMessageBase = TypeVar("TMessageBase", bound=MessageBase)


class MessageQuery(MessageBase):
    """
    Represents the query of a user to an agent
    """

    pass


class MessageResponse(MessageBase):
    """
    Represents the response to a user query
    It will be tied to citations that the LLM made to generate the response
    """

    pass


class Citation(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a citation for a part of a source_data, in an agent's response to a user query

    @param id: the id of the citation
    @param source_data_id: the id of the source_data where the citation is
    @param citation_metadata: the position of the citation in the source_data; TODO: meant to be a json formatted string
    @param message_response: the agent's response this citation is associated with
    """

    id: int
    citation_metadata: str

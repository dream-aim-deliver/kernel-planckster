from enum import Enum
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import uuid4


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


class User(BaseKernelPlancksterModel):
    """
    Represents a user in the system

    @param planckster_user_uuid: the id of the user
    """

    planckster_user_uuid: str

    def __str__(self) -> str:
        return "User: " + super().__str__() + f", planckster_user_uuid: {self.planckster_user_uuid}"


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
    @param knowledge_source: the knowledge source associated with this source_data
    """

    id: int
    name: str
    type: str
    lfn: str
    protocol: ProtocolEnum
    knowledge_source: KnowledgeSource

    def __str__(self) -> str:
        return (
            "SourceData: "
            + super().__str__()
            + f", id: {self.id}, name: {self.name}, lfn: {self.lfn}, protocol: {self.protocol}"
        )


class EmbeddingModel(BaseModel):
    """
    An embedding model is a model that can be used to embed a vector storde associated with a research context (including its source data), into a vector space

    @param id: the id of the embedding model
    @param name: the name of the embedding model
    """

    id: int
    name: str


class LLM(BaseModel):
    """
    A LLM (Language Learning Model) is a model that can be used to generate a response to a user query, given a vectorized research context

    @param id: the id of the LLM
    @param name: the name of the LLM
    @param embedding_models: the embedding models associated with this LLM
    """

    id: int
    llm_name: str
    embedding_models: List[EmbeddingModel]


class ResearchContext(BaseModel):
    """
    A research context belongs to a research topic, and is defined using a subset of the collection of source_data of the research topic
    This is the context in which conversations will happen

    @param id: the id of the research context
    @param title: the title of the research context
    @param planckster_tagger_node_id: the id of the planckster tagger node associated to this research context
    @param user: the user this research context belongs to
    @param llm: the LLM associated to this research context
    @param source_data: the source data associated to this research context
    """

    id: int
    title: str
    planckster_tagger_node_id: str
    user: User
    llm: LLM
    source_data: List[SourceData]


class VectorStore(BaseModel):
    """
    Represents a vector store, a vectorization of a research context to be inputted to an LLM

    @param id: the id of the vector store
    @param name: the name of the vector store
    @param lfn: the logical file name of the vector store
    @param protocol: the protocol used to store the vector store
    @param research_context: the research context this vector store is associated with
    @param embedding_model: the embedding model used to generate the vector store
    """

    id: int
    name: str
    lfn: str
    protocol: ProtocolEnum
    research_context: ResearchContext
    embedding_model: EmbeddingModel


class Conversation(BaseModel):
    """
    Represents a conversation between a user and an agent, within in a research context
    This is where messages will be exchanged

    @param id: the id of the conversation
    @param title: the title of the conversation
    @param research_context: the research context this conversation is associated with
    """

    id: int
    title: str
    research_context: ResearchContext


class MessageBase(BaseSoftDeleteKernelPlancksterModel):
    """
    Base class for user queries and agent responses

    @param id: the id of the message
    @param content: the content of the message
    @param timestamp: the datetime when the message was sent
    @param conversation: the conversation this message is associated with
    """

    id: int
    content: str
    timestamp: datetime
    conversation: Conversation


class MessageQuery(MessageBase):
    """
    Represents the query of a user to an agent

    @param user: the user that made the query
    """

    user: User


class MessageResponse(MessageBase):
    """
    Represents the response to a user query
    It will be tied to citations that the LLM made to generate the response
    """

    pass


class Citation(BaseModel):
    """
    Represents a citation for a part of a source_data, in an agent's response to a user query

    @param id: the id of the citation
    @param source_data_id: the id of the source_data where the citation is
    @param citation_metadata: the position of the citation in the source_data; TODO: meant to be a json formatted string
    @param message_response: the agent's response this citation is associated with
    """

    id: int
    source_data: SourceData
    citation_metadata: str
    message_response: MessageResponse

from enum import Enum
import os
import re
from pydantic import BaseModel, field_validator, model_validator
from typing import TypeVar, List
from datetime import datetime


class ProtocolEnum(Enum):
    """
    Enum for the different protocols that can be used to store a source_data.

    S3: the source_data is stored in an S3 bucket
    NAS: the source_data is stored in a NAS
    LOCAL: the source_data is stored locally
    """

    S3 = "s3"
    NAS = "nas"
    LOCAL = "local"


class SourceDataStatusEnum(Enum):
    """
    Enum for the different status that a source data can have.

    CREATED: the source data has been created
    UNAVAILABLE: the source data is not available
    AVAILABLE: the source data is available and part of a consistent dataset
    INCONSISTENT_DATASET: the source data is available but part of an inconsistent dataset
    """

    CREATED = "created"
    UNAVAILABLE = "unavailable"
    AVAILABLE = "available"
    INCONSISTENT_DATASET = "inconsistent_dataset"


class BaseKernelPlancksterModel(BaseModel):
    """
    Base class for all models in the project

    @param created_at: the datetime when the model was created
    @param updated_at: the datetime when the model was last updated
    """

    created_at: datetime
    updated_at: datetime

    def to_json(cls) -> str:
        """
        Dumps the model to a json formatted string. Wrapper around pydantic's model_dump_json method: in case they decide to deprecate it, we only refactor here.
        """
        return cls.model_dump_json()

    def __str__(self) -> str:
        return self.to_json()


class BaseSoftDeleteKernelPlancksterModel(BaseKernelPlancksterModel):
    """
    Base class for all models in the project that can be soft deleted

    @param deleted: whether the model is deleted or not
    @param deleted_at: the datetime when the model was deleted
    """

    deleted: bool
    deleted_at: datetime | None


class Client(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a human user, or any other entity (agent or program) that can interact with Kernel Planckster

    @param id: the id of the client
    @type id: int
    @param sub: the name of the client
    @type sub: str
    """

    id: int
    sub: str


class SourceData(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a source_data or a file

    @param id: the id of the source_data
    @param name: the name of the source_data
    @param relative_path: the relative path of the source_data
    @param type: the type of the source_data (e.g., txt, pdf, csv, etc.); inferred from the extension of the relative_path
    @param protocol: the protocol used to store the source_data
    @param status: the status of the source_data
    """

    id: int
    name: str
    relative_path: str
    type: str
    protocol: ProtocolEnum
    status: SourceDataStatusEnum

    @classmethod
    def from_json(cls, json_str: str) -> "SourceData":
        """
        Loads the model from a json formatted string. Wrapper around pydantic's model_validate_json method: in case they decide to deprecate it, we only refactor here.
        """
        return cls.model_validate_json(json_data=json_str)

    @classmethod
    def name_validation(cls, v: str) -> str:
        if v == "":
            raise ValueError("The name must not be empty")
        return v

    @classmethod
    def relative_path_validation(cls, v: str) -> str:
        value_error_flag = False
        value_error_msg = ""

        if v == "":
            value_error_msg += f"The relative path must not be empty. "
            raise ValueError(value_error_msg)

        v2 = re.sub(r"[^a-zA-Z0-9_\./-]", "", v)
        if v != v2:
            value_error_flag = True
            value_error_msg += f"The relative path must contain only alphanumeric characters, underscores, slashes, and dots. Other characters are not allowed. "

        ext = os.path.splitext(v)[1].replace(".", "")
        if ext == "":
            value_error_flag = True
            value_error_msg += f"The relative path provided did not have an extension. Extensions are required to infer the type of the source data. "

        first_char = v[0]
        if first_char == "/":
            value_error_flag = True
            value_error_msg += f"The relative path provided must not start with a slash. "

        if value_error_flag:
            value_error_msg += f"\nThe relative path provided was: '{v}'"
            raise ValueError(value_error_msg)

        return v

    @classmethod
    def protocol_validation(cls, v: str) -> ProtocolEnum:
        all_protocols = [e for e in ProtocolEnum]
        all_protocols_str = [p.value for p in all_protocols]
        implemented_protocols = [ProtocolEnum.S3]
        implemented_protocols_str = [p.value for p in implemented_protocols]

        try:
            enum = ProtocolEnum(v)
        except ValueError:
            raise ValueError(
                f"'{v}' is not a valid protocol. Valid protocols are:\n{all_protocols_str}\nImplemented protocols are:\n{implemented_protocols_str}"
            )

        if enum not in implemented_protocols:
            raise ValueError(
                f"The protocol '{v}' is not implemented. Please use one of the following: {implemented_protocols_str}"
            )

        return ProtocolEnum(v)

    @classmethod
    def populate_type(cls, v: str) -> str:
        basename = os.path.basename(v)
        ext_dot = os.path.splitext(basename)[1]
        ext = ext_dot.replace(".", "")
        return ext

    @field_validator("name")
    def name_must_not_be_empty(cls, v: str) -> str:
        return cls.name_validation(v)

    @field_validator("relative_path")
    def relative_path_must_be_correctly_formatted(cls, v: str) -> str:
        return cls.relative_path_validation(v)

    @field_validator("protocol")
    def protocol_must_be_supported(cls, v: ProtocolEnum) -> ProtocolEnum:
        return cls.protocol_validation(v.value)

    @model_validator(mode="before")
    def autofill_type(
        cls, values: dict[str, int | str | ProtocolEnum | SourceDataStatusEnum]
    ) -> dict[str, int | str | ProtocolEnum | SourceDataStatusEnum]:
        if "relative_path" in values:
            relative_path = values.get("relative_path")
            if isinstance(relative_path, str):
                values["type"] = cls.populate_type(relative_path)
        return values


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
    @param description: the description of the research context
    """

    id: int
    title: str
    description: str


class VectorStore(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a vector store, a vectorization of a research context to be inputted to an LLM

    @param id: the id of the vector store
    @param name: the name of the vector store
    @param lfn: the logical file name of the vector store
    """

    id: int
    name: str


class Conversation(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a conversation between a user and an agent, within in a research context
    This is where messages will be exchanged

    @param id: the id of the conversation
    @param title: the title of the conversation
    """

    id: int
    title: str


class MessageSenderTypeEnum(Enum):
    """
    Enum for the different types of sender of messages

    USER: the sender is a user
    AGENT: the sender is an agent
    """

    USER = "user"
    AGENT = "agent"


class MessageContentTypeEnum(Enum):
    """
    Enum for the different types of message content

    TEXT: the message content is text
    IMAGE: the message content is an image
    """

    TEXT = "text"
    IMAGE = "image"
    CITATION = "citation"


class BaseMessageContent(BaseModel):
    """
    Represents a piece of content that can be part of a message.

    @param id: the ID of the message content
    @type id: int
    @param ontent: the content of the message
    @type content: str
    """

    content: str
    content_type: MessageContentTypeEnum


class MessageContent(BaseMessageContent, BaseSoftDeleteKernelPlancksterModel):
    """
    Represents the pieces of content that can comprise an existing message.
    """

    id: int


class MessageBase(BaseSoftDeleteKernelPlancksterModel):
    """
    Base class for user queries and agent responses

    @param id: the id of the message
    @type id: int
    @param timestamp: the datetime when the message was sent
    @type timestamp: datetime
    @param sender: the name of the sender of the message
    @type sender: str
    @param sender_type: the type of the sender of the message
    @type sender_type: MessageSenderTypeEnum
    @param message_contents: A list of the content pieces of the message
    @type message_contents: List[MessageContent]
    """

    id: int
    timestamp: datetime
    thread_id: int
    sender: str
    sender_type: MessageSenderTypeEnum
    message_contents: List[MessageContent]


TMessageBase = TypeVar("TMessageBase", bound=MessageBase)


class UserMessage(MessageBase):
    """
    Represents the query of a user to an agent
    """

    sender_type: MessageSenderTypeEnum = MessageSenderTypeEnum.USER


class AgentMessage(MessageBase):
    """
    Represents the response to a user query
    It will be tied to citations that the LLM made to generate the response, and to an LLM directly
    """

    sender_type: MessageSenderTypeEnum = MessageSenderTypeEnum.AGENT


class Citation(BaseSoftDeleteKernelPlancksterModel):
    """
    Represents a citation for a part of a source_data, in an agent's response to a user query

    @param id: the id of the citation
    @param citation_metadata: the position of the citation in the source_data; TODO: meant to be a json formatted string
    """

    id: int
    citation_metadata: str

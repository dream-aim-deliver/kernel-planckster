from lib.core.entity.models import Conversation
from lib.core.ports.primary.list_conversations_primary_ports import ListConversationsInputPort
from lib.core.usecase_models.list_conversations_usecase_models import (
    ListConversationsError,
    ListConversationsRequest,
    ListConversationsResponse,
)


class ListConversationsUseCase(ListConversationsInputPort):
    def execute(self, request: ListConversationsRequest) -> ListConversationsResponse | ListConversationsError:
        research_context_id = request.research_context_id
        conversation_1 = Conversation(
            id=1,
            title="Conversation 1",
            created_at="2021-01-01 00:00:00",
            updated_at="2021-01-01 00:00:00",
            deleted=False,
            deleted_at=None,
            conversation_name="Conversation 1",
            research_context_id=request.research_context_id,
        )
        conversation_2 = Conversation(
            id=2,
            title="Conversation 2",
            created_at="2021-01-01 00:00:00",
            updated_at="2021-01-01 00:00:00",
            deleted=False,
            deleted_at=None,
            conversation_name="Conversation 2",
            research_context_id=request.research_context_id,
        )
        return ListConversationsResponse(
            research_context_id=research_context_id, conversations=[conversation_1, conversation_2]
        )


# class AlphaInitUserDTO(BaseDTO[User]):
# """
# A DTO for the initialization of a (hard coded) new user for the alpha release

# @param user_id: The id of the new user
# @type user_id: int | None
# """

# user_id: int | None = None

# def alpha_init(self) -> AlphaInitUserDTO:
# """
# Initializes a hard-coded new user with a single research context for the alpha release demo.
# If the user already exists, it will return the id of the existing user.

# @return: A DTO containing the result of the operation.
# @rtype: AlphaInitUserDTO
# """

# alpha_parameters = {
# "llm_name": "Alpha Dummy LLM",
# "research_context_title": "Alpha Research Context",
# "user_sid": "Alpha User"
# }

# sqla_user_query: SQLAUser | None = self.session.get(SQLAUser, alpha_parameters["user_sid"])

# if sqla_user_query is not None:
# return AlphaInitUserDTO(status=True, user_id=sqla_user_query.id)

# sqla_research_context_alpha = SQLAResearchContext(
# title=alpha_parameters["research_context"],
# source_data=[],
# )

# sqla_llm_alpha = SQLALLM(
# llm_name=alpha_parameters["llm_name"],
# research_contexts=[sqla_research_context_alpha],
# )

# sqla_user_alpha = SQLAUser(
# sid=alpha_parameters["user_sid"],
# research_contexts=[sqla_research_context_alpha],
# )

# try:
# sqla_research_context_alpha.save(session=self.session)
# self.session.commit()

# return AlphaInitUserDTO(status=True, user_id=sqla_research_context_alpha.user_id)

# except Exception as e:
# self.logger.error(f"Error while creating new user: {e}")
# errorDTO = AlphaInitUserDTO(
# status=False,
# errorCode=-1,
# errorMessage=f"Error while creating new user: {e}",
# errorName="Error while creating new user",
# errorType="ErrorWhileCreatingNewUser",
# )
# self.logger.error(f"{errorDTO}")
# return errorDTO

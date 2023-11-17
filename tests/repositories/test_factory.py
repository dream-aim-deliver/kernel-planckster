from lib.infrastructure.repository.sqla.models import SQLAConversation
from tests.fixtures.factory.sqla_model_factory import SQLATemporaryModelFactory


def test_list_research_context_conversations(
    sqla_temp_model_factory: SQLATemporaryModelFactory,
) -> None:
    sqla_conversation: SQLAConversation = sqla_temp_model_factory.make_conversation(n_messages=10)
    assert sqla_conversation is not None

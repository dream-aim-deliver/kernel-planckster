import random
import uuid
from faker import Faker
from lib.core.usecase.extend_research_context_usecase import ExtendResearchContextUseCase
from lib.core.usecase_models.extend_research_context_models import (
    ExtendResearchContextRequest,
    ExtendResearchContextResponse,
)
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAResearchContext,
    SQLAClient,
)


def test_extend_research_context(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_research_context: SQLAClient,
) -> None:
    usecase: ExtendResearchContextUseCase = app_initialization_container.extend_research_context_feature.usecase()

    assert usecase is not None

    client_with_context = fake_client_with_research_context
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_context.research_contexts,
    )

    assert len(client_with_context.research_contexts) > 1

    existing_research_context = random.choice(client_with_context.research_contexts)
    remaining_research_contexts = [
        rc for rc in client_with_context.research_contexts if rc.id != existing_research_context.id
    ]
    new_research_context = random.choice(remaining_research_contexts)
    # Make titles unique to query later
    existing_research_context_title = f"{existing_research_context.title}-{uuid.uuid4()}"
    existing_research_context.title = existing_research_context_title

    with db_session() as session:
        client_with_context.save(session=session, flush=True)
        session.commit()

    # Details for new Research Context data
    new_research_context_title = f"{new_research_context.title}-{uuid.uuid4()}"
    new_research_context_description = f"{fake.text()}-{uuid.uuid4()}"
    new_source_data_list = new_research_context.source_data
    new_source_data_ids = [sd.id for sd in new_source_data_list]

    with db_session() as session:
        queried_existing_research_context = (
            session.query(SQLAResearchContext).filter_by(title=existing_research_context_title).first()
        )

        assert queried_existing_research_context is not None

        request = ExtendResearchContextRequest(
            new_research_context_title=new_research_context_title,
            new_research_context_description=new_research_context_description,
            client_sub=fake_client_with_research_context.sub,
            llm_name=llm,
            new_source_data_ids=new_source_data_ids,
            existing_research_context_id=queried_existing_research_context.id,
        )
        response = usecase.execute(request=request)

        assert response is not None
        assert isinstance(response, ExtendResearchContextResponse)

        assert response.research_context is not None

        queried_new_research_context = session.get(SQLAResearchContext, response.research_context.id)

        assert queried_new_research_context is not None

        queried_new_research_context_source_data_list = queried_new_research_context.source_data
        queried_new_research_context_source_data_ids = [sd.id for sd in queried_new_research_context_source_data_list]

        existing_source_data_overlap_check = [
            sd.id
            for sd in queried_existing_research_context.source_data
            if sd.id not in queried_new_research_context_source_data_ids
        ]

        assert len(existing_source_data_overlap_check) == 0

        new_source_data_overlap_check = [
            sd_id for sd_id in new_source_data_ids if sd_id not in queried_new_research_context_source_data_ids
        ]

        assert len(new_source_data_overlap_check) == 0

        # Check uniqueness
        assert len(queried_new_research_context_source_data_ids) == len(
            set(queried_new_research_context_source_data_ids)
        )

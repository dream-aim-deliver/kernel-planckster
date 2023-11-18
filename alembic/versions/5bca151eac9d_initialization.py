"""Initialization

Revision ID: 5bca151eac9d
Revises: 
Create Date: 2023-11-18 13:03:13.350075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bca151eac9d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # For each polymorphic child (messages), we need to manually delete all the sa.CheckConstraint(...) lines
    op.create_table('embedding_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('CREATED_AT IS NOT NULL', name='EMBEDDING_MODEL_CREATED_NN'),
    sa.CheckConstraint('DELETED IS NOT NULL', name='EMBEDDING_MODEL_DELETED_NN'),
    sa.CheckConstraint('UPDATED_AT IS NOT NULL', name='EMBEDDING_MODEL_UPDATED_NN'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    mysql_engine='InnoDB'
    )
    op.create_table('knowledge_source',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('content_metadata', sa.String(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('CREATED_AT IS NOT NULL', name='KNOWLEDGE_SOURCE_CREATED_NN'),
    sa.CheckConstraint('DELETED IS NOT NULL', name='KNOWLEDGE_SOURCE_DELETED_NN'),
    sa.CheckConstraint('UPDATED_AT IS NOT NULL', name='KNOWLEDGE_SOURCE_UPDATED_NN'),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_table('llm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('llm_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('CREATED_AT IS NOT NULL', name='LLM_CREATED_NN'),
    sa.CheckConstraint('UPDATED_AT IS NOT NULL', name='LLM_UPDATED_NN'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('llm_name'),
    mysql_engine='InnoDB'
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sid', sa.String(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('CREATED_AT IS NOT NULL', name='USER_CREATED_NN'),
    sa.CheckConstraint('DELETED IS NOT NULL', name='USER_DELETED_NN'),
    sa.CheckConstraint('UPDATED_AT IS NOT NULL', name='USER_UPDATED_NN'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sid'),
    mysql_engine='InnoDB'
    )
    op.create_table('embedding_model_llm_association',
    sa.Column('embedding_model_id', sa.Integer(), nullable=True),
    sa.Column('llm_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['embedding_model_id'], ['embedding_model.id'], ),
    sa.ForeignKeyConstraint(['llm_id'], ['llm.id'], )
    )
    op.create_table('research_context',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('llm_id', sa.Integer(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('CREATED_AT IS NOT NULL', name='RESEARCH_CONTEXT_CREATED_NN'),
    sa.CheckConstraint('DELETED IS NOT NULL', name='RESEARCH_CONTEXT_DELETED_NN'),
    sa.CheckConstraint('UPDATED_AT IS NOT NULL', name='RESEARCH_CONTEXT_UPDATED_NN'),
    sa.ForeignKeyConstraint(['llm_id'], ['llm.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_table('source_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('lfn', sa.String(), nullable=False),
    sa.Column('protocol', sa.Enum('S3', 'NAS', 'LOCAL', name='protocolenum'), nullable=False),
    sa.Column('knowledge_source_id', sa.Integer(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('CREATED_AT IS NOT NULL', name='SOURCE_DATA_CREATED_NN'),
    sa.CheckConstraint('DELETED IS NOT NULL', name='SOURCE_DATA_DELETED_NN'),
    sa.CheckConstraint('UPDATED_AT IS NOT NULL', name='SOURCE_DATA_UPDATED_NN'),
    sa.ForeignKeyConstraint(['knowledge_source_id'], ['knowledge_source.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('lfn'),
    mysql_engine='InnoDB'
    )
    op.create_table('conversation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('research_context_id', sa.Integer(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('CREATED_AT IS NOT NULL', name='CONVERSATION_CREATED_NN'),
    sa.CheckConstraint('DELETED IS NOT NULL', name='CONVERSATION_DELETED_NN'),
    sa.CheckConstraint('UPDATED_AT IS NOT NULL', name='CONVERSATION_UPDATED_NN'),
    sa.ForeignKeyConstraint(['research_context_id'], ['research_context.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_table('source_data_research_context_association',
    sa.Column('source_data_id', sa.Integer(), nullable=True),
    sa.Column('research_context_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['research_context_id'], ['research_context.id'], ),
    sa.ForeignKeyConstraint(['source_data_id'], ['source_data.id'], )
    )
    op.create_table('vector_store',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('lfn', sa.String(), nullable=False),
    sa.Column('protocol', sa.Enum('S3', 'NAS', 'LOCAL', name='protocolenum'), nullable=False),
    sa.Column('research_context_id', sa.Integer(), nullable=True),
    sa.Column('embedding_model_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('CREATED_AT IS NOT NULL', name='VECTOR_STORE_CREATED_NN'),
    sa.CheckConstraint('UPDATED_AT IS NOT NULL', name='VECTOR_STORE_UPDATED_NN'),
    sa.ForeignKeyConstraint(['embedding_model_id'], ['embedding_model.id'], ),
    sa.ForeignKeyConstraint(['research_context_id'], ['research_context.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('lfn'),
    mysql_engine='InnoDB'
    )
    op.create_table('message_base',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('conversation_id', sa.Integer(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('CREATED_AT IS NOT NULL', name='MESSAGE_BASE_CREATED_NN'),
    sa.CheckConstraint('DELETED IS NOT NULL', name='MESSAGE_BASE_DELETED_NN'),
    sa.CheckConstraint('UPDATED_AT IS NOT NULL', name='MESSAGE_BASE_UPDATED_NN'),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_table('message_query',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['message_base.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_table('message_response',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['message_base.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_table('citation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_data_id', sa.Integer(), nullable=False),
    sa.Column('citation_metadata', sa.String(), nullable=False),
    sa.Column('message_response_id', sa.Integer(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.CheckConstraint('CREATED_AT IS NOT NULL', name='CITATION_CREATED_NN'),
    sa.CheckConstraint('DELETED IS NOT NULL', name='CITATION_DELETED_NN'),
    sa.CheckConstraint('UPDATED_AT IS NOT NULL', name='CITATION_UPDATED_NN'),
    sa.ForeignKeyConstraint(['message_response_id'], ['message_response.id'], ),
    sa.ForeignKeyConstraint(['source_data_id'], ['source_data.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('citation')
    op.drop_table('message_response')
    op.drop_table('message_query')
    op.drop_table('message_base')
    op.drop_table('vector_store')
    op.drop_table('source_data_research_context_association')
    op.drop_table('conversation')
    op.drop_table('source_data')
    op.drop_table('research_context')
    op.drop_table('embedding_model_llm_association')
    op.drop_table('user')
    op.drop_table('llm')
    op.drop_table('knowledge_source')
    op.drop_table('embedding_model')
    # These were added by hand
    # We need to manually drop the enums created in the upgrade
    sa_enum_protocolenum = sa.Enum(name="protocolenum")
    sa_enum_protocolenum.drop(op.get_bind(), checkfirst=True)  # type: ignore    # ### end Alembic commands ###

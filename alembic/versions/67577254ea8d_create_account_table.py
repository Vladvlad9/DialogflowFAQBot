"""create account table

Revision ID: 67577254ea8d
Revises: 
Create Date: 2023-05-04 12:55:53.069511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67577254ea8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.BIGINT(), nullable=False),
                    sa.Column('user_id', sa.BIGINT(), nullable=False),
                    sa.Column('specialist', sa.BOOLEAN(), default=False),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('users')

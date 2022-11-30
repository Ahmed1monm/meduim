"""article to tags table

Revision ID: 69286417ec96
Revises: e2b60604c971
Create Date: 2022-11-30 17:00:41.340167

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '69286417ec96'
down_revision = 'e2b60604c971'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('article_to_tags',
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True)
                    )


def downgrade() -> None:
    pass

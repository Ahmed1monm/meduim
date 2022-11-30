"""create tags table

Revision ID: e2b60604c971
Revises: ced82c0235d6
Create Date: 2022-11-30 16:27:11.246941

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e2b60604c971'
down_revision = 'ced82c0235d6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('tags',
                    sa.Column(
                        'id',
                        sa.Integer,
                        primary_key=True,
                        nullable=False
                    ),
                    sa.Column(
                        'name',
                        sa.String,
                        nullable=False
                    )
                    )


def downgrade() -> None:
    pass

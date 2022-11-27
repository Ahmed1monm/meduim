"""create phone number  for auther col

Revision ID: ced82c0235d6
Revises: 
Create Date: 2022-11-26 01:45:56.513988

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ced82c0235d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('authers', sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    pass

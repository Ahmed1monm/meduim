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
    op.create_table(
        'article_to_tags',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('article_id', sa.Integer, sa.ForeignKey('articles.id')),
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tags.id')),

    )

    op.create_table(
        'authors_to_tags',
        sa.Column('id', sa.Integer, primary_key=True, ),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('authers.id')),
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tags.id')),

    )


def downgrade() -> None:
    pass

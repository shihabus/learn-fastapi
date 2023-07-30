"""add content column to posts table

Revision ID: 2600ce059353
Revises: 6ca93b8f9bf1
Create Date: 2023-07-30 21:41:05.089199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2600ce059353"
down_revision = "6ca93b8f9bf1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass

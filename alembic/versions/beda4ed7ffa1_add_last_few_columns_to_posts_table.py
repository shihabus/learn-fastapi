"""add last few columns to posts table

Revision ID: beda4ed7ffa1
Revises: b79a5144f59d
Create Date: 2023-07-30 21:48:17.439957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "beda4ed7ffa1"
down_revision = "b79a5144f59d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass

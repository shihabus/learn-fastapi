"""add foreign-key to posts table

Revision ID: b79a5144f59d
Revises: 7bbd3f0b05ba
Create Date: 2023-07-30 21:47:18.901509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b79a5144f59d"
down_revision = "7bbd3f0b05ba"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass

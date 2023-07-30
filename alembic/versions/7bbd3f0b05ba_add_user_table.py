"""add user table

Revision ID: 7bbd3f0b05ba
Revises: 2600ce059353
Create Date: 2023-07-30 21:41:49.475636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7bbd3f0b05ba"
down_revision = "2600ce059353"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass

"""autogenerate add phone_number column to User table

Revision ID: 8cdc7ff12291
Revises: 5852a6d5f882
Create Date: 2023-07-30 22:00:49.878293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cdc7ff12291'
down_revision = '5852a6d5f882'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###

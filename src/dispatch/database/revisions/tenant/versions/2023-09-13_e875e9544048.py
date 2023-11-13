"""Adds canary column to signal_instance

Revision ID: e875e9544048
Revises: 0560fab4537f
Create Date: 2023-09-13 09:31:24.223488

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "e875e9544048"
down_revision = "0560fab4537f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("signal_instance", sa.Column("canary", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("signal_instance", "canary")

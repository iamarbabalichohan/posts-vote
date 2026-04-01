"""Add content column to posts table

Revision ID: b0598c41b5f6
Revises: 4647aee02d56
Create Date: 2026-03-31 18:31:13.213168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0598c41b5f6'
down_revision = '4647aee02d56'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

"""Add foreign key to posts table

Revision ID: 11cb9a82bed8
Revises: 0d72ca65e7e2
Create Date: 2026-03-31 19:52:16.025020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11cb9a82bed8'
down_revision = '0d72ca65e7e2'
branch_labels = None
depends_on = None


def upgrade():
    # op.add_column('posts', sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False))
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass

"""Add users table

Revision ID: 0d72ca65e7e2
Revises: b0598c41b5f6
Create Date: 2026-03-31 18:43:00.909537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d72ca65e7e2'
down_revision = 'b0598c41b5f6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True, autoincrement=True),
                    sa.Column('email', sa.String, nullable=False, unique=True),
                    sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()'))
                    # ,sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email')  
                )
    pass


def downgrade():
    op.drop_table('users')
    pass

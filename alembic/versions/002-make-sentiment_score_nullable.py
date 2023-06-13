"""Make sentiment score nullable

Revision ID: 002
Revises:
Create Date: 2023-06-12 

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

revision = '002'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.drop_column('tweets', 'sentiment_score')
    op.add_column('tweets', sa.Column('sentiment_score', sa.Numeric(precision=10, scale=2), nullable=True))

def downgrade():
    op.drop_column('tweets', 'sentiment_score')
    op.add_column(sa.Column('sentiment_score', sa.Numeric(precision=10, scale=2), nullable=False)),


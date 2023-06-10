"""Create the first table

Revision ID: 001
Revises:
Create Date: 2023-06-09 

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'tweets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('tweeted_at', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('user', sa.String(100), nullable=False),
        sa.Column('body', sa.String(280), nullable=False),
        sa.Column('sentiment_score', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('ticker', sa.String(10), nullable=True)
    )


def downgrade():
    op.drop_table('tweets')

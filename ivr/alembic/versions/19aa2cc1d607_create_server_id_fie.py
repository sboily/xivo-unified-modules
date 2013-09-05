"""create server_id field

Revision ID: 19aa2cc1d607
Revises: None
Create Date: 2013-09-05 09:42:55.231224

"""

# revision identifiers, used by Alembic.
revision = '19aa2cc1d607'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('ivr', sa.Column('server_id', sa.Integer))


def downgrade():
    op.drop_column('ivr', 'server_id')

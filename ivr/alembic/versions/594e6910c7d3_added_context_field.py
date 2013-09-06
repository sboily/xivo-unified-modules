"""Added context field

Revision ID: 594e6910c7d3
Revises: 19aa2cc1d607
Create Date: 2013-09-06 09:23:37.967295

"""

# revision identifiers, used by Alembic.
revision = '594e6910c7d3'
down_revision = '19aa2cc1d607'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('ivr', sa.Column('context', sa.String(200)))


def downgrade():
    pass

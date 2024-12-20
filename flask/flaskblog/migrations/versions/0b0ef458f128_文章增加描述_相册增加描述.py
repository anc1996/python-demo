"""文章增加描述，相册增加描述

Revision ID: 0b0ef458f128
Revises: d54ff4cbc358
Create Date: 2024-10-21 23:55:27.732978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b0ef458f128'
down_revision = 'd54ff4cbc358'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_album', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_album', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###

"""修改railway

Revision ID: abacbe40adc5
Revises: 3da114049bab
Create Date: 2024-10-21 11:41:22.954806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abacbe40adc5'
down_revision = '3da114049bab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('db_passenger',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='主键'),
    sa.Column('name', sa.String(length=15), nullable=True, comment='姓名'),
    sa.Column('age', sa.Integer(), nullable=True, comment='年龄'),
    sa.Column('sex', sa.String(length=1), nullable=True, comment='性别'),
    sa.Column('email', sa.String(length=128), nullable=True, comment='邮箱地址'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('db_train',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='主键'),
    sa.Column('train_name', sa.String(length=15), nullable=True, comment='列车名称'),
    sa.Column('train_type', sa.String(length=15), nullable=True, comment='列车类型'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('db_passenger_ticket',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='主键'),
    sa.Column('passenger_id', sa.Integer(), nullable=True, comment='乘客id'),
    sa.Column('train_id', sa.Integer(), nullable=True, comment='列车id'),
    sa.ForeignKeyConstraint(['passenger_id'], ['db_passenger.id'], ),
    sa.ForeignKeyConstraint(['train_id'], ['db_train.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('db_passenger_ticket')
    op.drop_table('db_train')
    op.drop_table('db_passenger')
    # ### end Alembic commands ###

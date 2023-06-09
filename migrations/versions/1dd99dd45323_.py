"""empty message

Revision ID: 1dd99dd45323
Revises: 5d52f4ae6867
Create Date: 2023-04-17 21:20:24.163055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dd99dd45323'
down_revision = '5d52f4ae6867'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.String(length=250), nullable=True))
        batch_op.drop_column('image_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_id', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###

"""matching language table

Revision ID: d290b6bd9058
Revises: 8e80a4cdb778
Create Date: 2023-03-29 01:58:13.307433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd290b6bd9058'
down_revision = '8e80a4cdb778'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('matching_lang', sa.String(length=64), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('matching_lang')

    # ### end Alembic commands ###

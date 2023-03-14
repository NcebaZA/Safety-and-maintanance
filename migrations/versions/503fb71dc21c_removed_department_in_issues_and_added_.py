"""Removed department in issues and added in title column

Revision ID: 503fb71dc21c
Revises: 17283f0d3399
Create Date: 2023-03-14 21:51:16.378611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '503fb71dc21c'
down_revision = '17283f0d3399'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=255), nullable=True))
        batch_op.drop_column('department')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('department', sa.VARCHAR(length=35), nullable=True))
        batch_op.drop_column('title')

    # ### end Alembic commands ###

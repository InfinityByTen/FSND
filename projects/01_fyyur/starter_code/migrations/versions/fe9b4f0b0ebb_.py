"""empty message

Revision ID: fe9b4f0b0ebb
Revises: 7f9c8f9075e9
Create Date: 2020-01-22 20:07:12.959791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe9b4f0b0ebb'
down_revision = '7f9c8f9075e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=240), nullable=True))
    op.add_column('Artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'website_link')
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###

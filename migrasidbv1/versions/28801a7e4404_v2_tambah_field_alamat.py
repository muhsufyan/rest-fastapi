"""v2 tambah field alamat

Revision ID: 28801a7e4404
Revises: 444acb4ddc7b
Create Date: 2022-03-15 12:38:51.828078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28801a7e4404'
down_revision = '444acb4ddc7b'
branch_labels = None
depends_on = None


def upgrade():
    # tambah field baru yaitu alamat di tabel posts
    op.add_column('posts',sa.Column("alamat", sa.String, nullable=False))

def downgrade():
    op.drop_column('posts','alamat')

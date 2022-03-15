"""v1 create table posts

Revision ID: 444acb4ddc7b
Revises: 
Create Date: 2022-03-15 12:01:39.798711

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = '444acb4ddc7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # buat tabel posts
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                            sa.Column('nama', sa.String(), nullable=False),
                            sa.Column('umur', sa.Integer, nullable=False),
                            sa.Column("published", sa.Boolean, server_default="True", nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )


def downgrade():
    # hapus tabel posts
    op.drop_table('posts')

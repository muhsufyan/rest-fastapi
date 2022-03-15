"""v4 add foreign-key to posts table

Revision ID: 4575a1b53aed
Revises: c36de42a6607
Create Date: 2022-03-15 13:26:36.614637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4575a1b53aed'
down_revision = 'c36de42a6607'
branch_labels = None
depends_on = None


def upgrade():
    # tambah foreign key ke tabel posts yg berasal dari id users 
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')

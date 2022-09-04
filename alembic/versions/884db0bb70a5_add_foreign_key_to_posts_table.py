"""Add foreign-key to posts table

Revision ID: 884db0bb70a5
Revises: b1d1f867c228
Create Date: 2022-09-03 20:55:21.123581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '884db0bb70a5'
down_revision = 'b1d1f867c228'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """ 
    Add new column name 'owner_id' in 'posts' table 
    and create foreign key name 'post_users_fk '  
    """
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False)),
    op.create_foreign_key(
            constraint_name='post_users_fk',
            source_table= 'posts', 
            referent_table= 'users',
            local_cols=['owner_id'], 
            remote_cols=['id'], 
            ondelete="CASCADE"
      )
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", "posts")
    op.drop_column("posts", "owner_id")
    pass

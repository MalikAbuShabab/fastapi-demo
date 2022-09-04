"""Create posts table

Revision ID: d090d2d9128d
Revises: 
Create Date: 2022-08-17 18:36:57.278342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd090d2d9128d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
                                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                                    sa.Column('title',sa.String(),nullable=False)
                                    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass

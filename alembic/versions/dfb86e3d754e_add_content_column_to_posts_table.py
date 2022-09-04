"""Add content column to posts table

Revision ID: dfb86e3d754e
Revises: d090d2d9128d
Create Date: 2022-09-03 20:28:27.079163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfb86e3d754e'
down_revision = 'd090d2d9128d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(),nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

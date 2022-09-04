"""Add user table

Revision ID: b1d1f867c228
Revises: dfb86e3d754e
Create Date: 2022-09-03 20:39:26.848557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1d1f867c228'
down_revision = 'dfb86e3d754e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                                    sa.Column('id', sa.Integer(), nullable=False),
                                    sa.Column('email',sa.String(),nullable=False),
                                    sa.Column('password',sa.String(),nullable=False),
                                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                                        server_default=sa.text('now()'),nullable=False),
                                    sa.PrimaryKeyConstraint('id'),
                                    sa.UniqueConstraint('email')
                                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass

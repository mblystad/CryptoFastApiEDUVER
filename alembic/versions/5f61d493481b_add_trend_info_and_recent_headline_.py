"""Add trend_info and recent_headline fields

Revision ID: 5f61d493481b
Revises: 
Create Date: 2025-05-26 14:37:23.450359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f61d493481b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('crypto_metadata',
        sa.Column('trend_info', sa.String(length=255)),
        schema='reporting_schema'
    )
    op.add_column('crypto_metadata',
        sa.Column('recent_headline', sa.String(length=512)),
        schema='reporting_schema'
    )


def downgrade() -> None:
    op.drop_column('crypto_metadata', 'trend_info', schema='reporting_schema')
    op.drop_column('crypto_metadata', 'recent_headline', schema='reporting_schema')

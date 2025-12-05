"""
add rdp_file and avd_access_token to targets

Revision ID: b1c2d3e4f5a6
Revises: 2478611410c3
Create Date: 2025-11-27 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

from server.migrations.tenant import for_each_tenant_schema

revision = 'b1c2d3e4f5a6'
down_revision = '2478611410c3'
branch_labels = None
depends_on = None


@for_each_tenant_schema
def upgrade(schema: str = 'tenant') -> None:
    op.add_column(
        'targets',
        sa.Column('rdp_file', sa.String(), nullable=True),
        schema=schema,
    )
    op.add_column(
        'targets',
        sa.Column('avd_access_token', sa.String(), nullable=True),
        schema=schema,
    )


@for_each_tenant_schema
def downgrade(schema: str = 'tenant') -> None:
    # Use raw SQL with IF EXISTS to handle cases where columns don't exist
    op.execute(
        sa.text(f'ALTER TABLE {schema}.targets DROP COLUMN IF EXISTS avd_access_token')
    )
    op.execute(sa.text(f'ALTER TABLE {schema}.targets DROP COLUMN IF EXISTS rdp_file'))

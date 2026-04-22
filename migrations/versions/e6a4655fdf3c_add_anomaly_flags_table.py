"""add_anomaly_flags_table

Revision ID: e6a4655fdf3c
Revises: fd30fc0f6054
Create Date: 2026-04-22 15:07:34.768295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6a4655fdf3c'
down_revision: Union[str, Sequence[str], None] = 'fd30fc0f6054'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS anomaly_flags (
            symbol          VARCHAR NOT NULL REFERENCES instruments(symbol),
            timestamp       TIMESTAMPTZ NOT NULL,
            detected_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            daily_return    NUMERIC(10, 6),
            volume_ratio    NUMERIC(10, 6),
            price_gap       NUMERIC(10, 6),
            hl_range        NUMERIC(10, 6),
            return_zscore   NUMERIC(10, 6),
            iso_score       NUMERIC(10, 6),
            rule_flagged    BOOLEAN,
            iso_flagged     BOOLEAN,
            anomaly         BOOLEAN,
            PRIMARY KEY (symbol, timestamp)
        );
    """)

def downgrade():
    op.execute("DROP TABLE IF EXISTS anomaly_flags;")
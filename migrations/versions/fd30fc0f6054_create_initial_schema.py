"""create_initial_schema

Revision ID: fd30fc0f6054
Revises: 
Create Date: 2026-03-24 16:49:07.847641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fd30fc0f6054'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS instruments (
            symbol       VARCHAR PRIMARY KEY,
            name         VARCHAR,
            asset_class  VARCHAR,
            exchange     VARCHAR,
            created_at   TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS ohlcv_bars (
            symbol      VARCHAR NOT NULL REFERENCES instruments(symbol),
            timestamp   TIMESTAMPTZ NOT NULL,
            timespan    VARCHAR NOT NULL,
            open        NUMERIC(12,4),
            high        NUMERIC(12,4),
            low         NUMERIC(12,4),
            close       NUMERIC(12,4),
            volume      BIGINT,
            PRIMARY KEY (symbol, timestamp, timespan)
        );

        CREATE TABLE IF NOT EXISTS risk_snapshots (
            symbol                VARCHAR NOT NULL REFERENCES instruments(symbol),
            computed_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            period_start          TIMESTAMPTZ,
            period_end            TIMESTAMPTZ,
            volatility            NUMERIC(10,6),
            annualized_volatility NUMERIC(10,6),
            max_drawdown          NUMERIC(10,6),
            sharpe_ratio          NUMERIC(10,6),
            PRIMARY KEY (symbol, computed_at)
        );
    """)

def downgrade():
    op.execute("""
        DROP TABLE IF EXISTS risk_snapshots;
        DROP TABLE IF EXISTS ohlcv_bars;
        DROP TABLE IF EXISTS instruments;
    """)

# pylint: disable=invalid-name,no-member

"""seed arukereso xgimi mogo 4 laser

Revision ID: 202512140140
Revises: 202512140130
Create Date: 2025-12-14 01:40:38.473577

"""

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '202512140140'
down_revision: str = '202512140130'
branch_labels: str | list[str] | tuple[str, ...] | None = None
depends_on: str | list[str] | tuple[str, ...] | None = None


def upgrade() -> None:
    """
    Insert XGIMI MoGo 4 Laser watch target.
    """

    op.execute(
        """
        INSERT INTO watch_targets (
            name,
            url,
            selector_type,
            selector,
            processor_type,
            processor_config,
            active
        ) VALUES (
            'Árukereső – XGIMI MoGo 4 Laser',
            'https://www.arukereso.hu/projektor-c88/xgimi/mogo-4-laser-wk03k-p1208819068/',
            'css',
            '.row-price > span',
            'min_value',
            '{}',
            TRUE
        );
        """
    )


def downgrade() -> None:
    """
    Remove XGIMI MoGo 4 Laser watch target.
    """

    op.execute(
        """
        DELETE FROM watch_targets
        WHERE name = 'Árukereső – XGIMI MoGo 4 Laser';
        """
    )

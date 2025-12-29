# pylint: disable=invalid-name,no-member

"""rename raw_value columns

Revision ID: 202512280239
Revises: 202512140140
Create Date: 2025-12-28 02:39:15.721772

"""

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '202512280239'
down_revision: str = '202512140140'
branch_labels: str | list[str] | tuple[str, ...] | None = None
depends_on: str | list[str] | tuple[str, ...] | None = None


def upgrade() -> None:
    """
    Rename raw_value columns to raw_text.
    """

    op.alter_column(
        "watch_targets",
        "last_raw_value",
        new_column_name="last_raw_text",
    )

    op.alter_column(
        "watch_targets",
        "last_processed_value",
        new_column_name="last_processed_text",
    )

    op.alter_column(
        "watch_logs",
        "raw_value",
        new_column_name="raw_text",
    )

    op.alter_column(
        "watch_logs",
        "processed_value",
        new_column_name="processed_text",
    )


def downgrade() -> None:
    """
    Revert raw_text columns back to raw_value.
    """

    op.alter_column(
        "watch_targets",
        "last_raw_text",
        new_column_name="last_raw_value",
    )

    op.alter_column(
        "watch_targets",
        "last_processed_text",
        new_column_name="last_processed_value",
    )

    op.alter_column(
        "watch_logs",
        "raw_text",
        new_column_name="raw_value",
    )

    op.alter_column(
        "watch_logs",
        "processed_text",
        new_column_name="processed_value",
    )

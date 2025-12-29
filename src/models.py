# pylint: disable=too-few-public-methods

"""
Database models for the application.
"""

from datetime import datetime
from sqlalchemy import (
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    """


class WatchTarget(Base):
    """
    ORM model for watch targets.
    """

    __tablename__ = "watch_targets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    selector_type: Mapped[str] = mapped_column(
        String(10), nullable=False, default="css"
    )
    selector: Mapped[str] = mapped_column(Text, nullable=False)
    processor_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="raw_text"
    )
    processor_config: Mapped[dict[str, object] | None] = mapped_column(
        JSON, nullable=True
    )
    last_run_at: Mapped[datetime | None] = mapped_column(
      DateTime(timezone=True), nullable=True
    )
    last_status: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )
    last_raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_processed_text: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    logs: Mapped[list["WatchLog"]] = relationship(
        back_populates="target",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class WatchLog(Base):
    """
    ORM model for watch logs.
    """

    __tablename__ = "watch_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    watch_target_id: Mapped[int] = mapped_column(
        ForeignKey("watch_targets.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    run_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),  # pylint: disable=not-callable
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    processed_text: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    target: Mapped[WatchTarget] = relationship(
        back_populates="logs",
    )

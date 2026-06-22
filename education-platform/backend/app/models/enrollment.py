from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    school_class_id: Mapped[int] = mapped_column(
        ForeignKey("school_classes.id", ondelete="CASCADE"), primary_key=True
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), primary_key=True
    )
    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    student: Mapped["Student"] = relationship(back_populates="enrollments")
    school_class: Mapped["SchoolClass"] = relationship(back_populates="enrollments")

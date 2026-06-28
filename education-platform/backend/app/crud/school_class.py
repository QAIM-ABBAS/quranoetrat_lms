from __future__ import annotations

from app.crud.base import CRUDBase
from app.models.school_class import SchoolClass
from app.schemas.school_class import SchoolClassCreate, SchoolClassUpdate


class CRUDSchoolClass(
    CRUDBase[SchoolClass, SchoolClassCreate, SchoolClassUpdate]
):
    pass


school_class = CRUDSchoolClass(SchoolClass)

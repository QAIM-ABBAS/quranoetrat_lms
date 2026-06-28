import importlib

from app.db.base import Base
from app.db.session import engine

MODEL_MODULES = (
    "app.models.user",
    "app.models.teacher",
    "app.models.student",
    "app.models.school_class",
    "app.models.lesson",
    "app.models.enrollment",
)


def import_models() -> None:
    for module_name in MODEL_MODULES:
        importlib.import_module(module_name)


async def init_db() -> None:
    import_models()

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    import_models()

    async with engine.begin() as connection:
<<<<<<< HEAD
        await connection.run_sync(Base.metadata.drop_all)
=======
        await connection.run_sync(Base.metadata.drop_all)
>>>>>>> parent of dab17bb (Delete education-platform directory)

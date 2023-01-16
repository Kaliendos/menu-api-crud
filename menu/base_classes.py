from fastapi import Depends, HTTPException

from config.database.db import SessionLocal, get_session


class BaseOperation:
    """
    Базовый класс для операций.
    Предоставляет интрефейс сессии и  поиска объектов
    """
    def __init__(self, session: SessionLocal = Depends(get_session)):
        self.session = session

    def get_objects_list(self, model):
        """
        Получить список объектов,
        принимает параметр model в качестве модели
         """
        return (
            self.session
            .query(model)
            .all()
        )

    def get_object_or_404(self, model, object_id, not_found_message: str):
        """
        Получить объект по id, если объект не найден,
        то вызывет HTTPException404
        """
        obj_instance = self.session.query(model).get(object_id)
        if obj_instance is None:
            raise HTTPException(status_code=404, detail=not_found_message)
        return obj_instance

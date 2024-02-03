from django.shortcuts import get_object_or_404
from django.http import Http404

from celery_api.models import File


def update(file_id, new_value):
    """Обновляем поле processed у объекта модели по id."""
    try:
        file_obj = get_object_or_404(File, pk=file_id)
        print(f"Updating processed field for file_id {file_id} to {new_value}")
        file_obj.processed = new_value
        file_obj.save()
        return f"Значение поля файла успешно обновлено: {file_obj}"
    except Http404:
        return f"Файл с id {file_id} не найден в базе данных."

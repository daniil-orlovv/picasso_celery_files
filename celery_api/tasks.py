from picasso.celery import app
from celery_api.service import update


@app.task
def update_processed_field(file_id, new_value):
    """Задача для Celery по обновлению поля processed."""
    update(file_id, new_value)

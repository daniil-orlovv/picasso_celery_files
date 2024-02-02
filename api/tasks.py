from picasso.celery import app
from api.service import update


@app.task
def update_processed_field(file_id, new_value):
    update(file_id, new_value)

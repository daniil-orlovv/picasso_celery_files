from django.db import models


class File(models.Model):
    """Модель для хранения файлов, отправленных по API."""
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

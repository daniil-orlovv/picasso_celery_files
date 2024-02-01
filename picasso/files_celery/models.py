from django.db import models


class File(models.Model):
    file = models.FileField()
    uploaded_at = models.DateTimeField()
    processed = models.BooleanField

from rest_framework import serializers

from celery_api.models import File


class FileSerializer(serializers.ModelSerializer):
    """Сериализуем данные API."""
    file = serializers.FileField()

    class Meta:
        model = File
        fields = ('id', 'file', 'uploaded_at', 'processed')

from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = File
        fields = ('id', 'file', 'uploaded_at', 'processed')

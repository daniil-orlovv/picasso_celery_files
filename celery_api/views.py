from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.exceptions import Retry

from celery_api.models import File
from celery_api.serializers import FileSerializer
from celery_api.tasks import update_processed_field


class FilesAPIList(APIView):

    def get(self, request):
        cats = File.objects.all()
        serializer = FileSerializer(cats, many=True)
        return Response(serializer.data)


class FilesAPICreate(APIView):

    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file_instance = serializer.save()

            try:
                update_processed_field.delay(file_instance.id, True)
            except Retry:
                return Response(
                    {'error': 'Ошибка при отправке задачи в Celery'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

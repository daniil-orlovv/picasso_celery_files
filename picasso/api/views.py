from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from files.models import File
from api.serializers import FileSerializer
from api.tasks import update_processed_field


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
            update_processed_field.delay(file_instance.id, True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.urls import path

from celery_api.views import FilesAPICreate, FilesAPIList

urlpatterns = [
    path('files/', FilesAPIList.as_view(), name='files'),
    path('upload/', FilesAPICreate.as_view(), name='upload'),
]

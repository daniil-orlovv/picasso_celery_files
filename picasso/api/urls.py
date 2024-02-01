from django.urls import path

from api.views import FilesAPICreate, FilesAPIList

urlpatterns = [
    path('files/', FilesAPIList.as_view(), name='files'),
    path('upload/', FilesAPICreate.as_view(), name='upload'),
]

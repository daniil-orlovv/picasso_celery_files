from http import HTTPStatus
import shutil
import tempfile

from django.test import TestCase, Client, override_settings
from django.conf import settings
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from dateutil import parser
from datetime import datetime

from celery_api.models import File


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestEndpoint(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.files = [
            File(
                file='File1.txt',
                uploaded_at=timezone.now(),
                processed=False
            ),
            File(
                file='File2.txt',
                uploaded_at=timezone.now(),
                processed=False
            ),
            File(
                file='File3.txt',
                uploaded_at=timezone.now(),
                processed=False
            ),
        ]
        cls.file_content = b'Text'
        cls.uploaded_file = SimpleUploadedFile("file.txt", cls.file_content)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()

    def test_endpoint_files(self):
        """Проверем, что эндпоинт files/ возвращает код ответа 200 и что типы
        данных в ответе json соответствует ожидаемым.
        """
        response = self.guest_client.get('/api/files/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        File.objects.bulk_create(self.files)
        json_data = response.json()
        for item in json_data:
            self.assertTrue(isinstance(item.get('id'), int))
            self.assertTrue(isinstance(item.get('file'), str))
            uploaded_at_str = item.get('uploaded_at')
            uploaded_at = parser.isoparse(uploaded_at_str)
            self.assertTrue(isinstance(uploaded_at, datetime))
            self.assertTrue(isinstance(item.get('processed'), bool))

    def test_endpoint_upload(self):
        """Проверем, что эндпоинт upload/ возвращает код ответа 201 и что типы
        данных в ответе json соответствует ожидаемым.
        """
        data = {
            "file": self.uploaded_file
        }

        response = self.guest_client.post('/api/upload/', data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        json_data = response.json()
        self.assertTrue(isinstance(json_data.get('id'), int))
        self.assertTrue(isinstance(json_data.get('file'), str))
        uploaded_at_str = json_data.get('uploaded_at')
        uploaded_at = parser.isoparse(uploaded_at_str)
        self.assertTrue(isinstance(uploaded_at, datetime))
        self.assertTrue(isinstance(json_data.get('processed'), bool))

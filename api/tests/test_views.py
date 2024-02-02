from django.test import TestCase, Client
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from files.models import File


class YourApiViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.file_content = b'Text'
        cls.uploaded_file = SimpleUploadedFile("file.txt", cls.file_content)

    def setUp(self):
        self.client = Client()

    def test_post_method(self):
        """Проверем, что метод post при загрузке файла возвращает
        код ответа 201 и что количество объектов модели File равно 1.
        """
        data = {'file': self.uploaded_file}
        response = self.client.post(
            '/api/upload/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 1)

    def test_post_method_with_invalid_data(self):
        """Проверем, что метод post при отсутствии файла возвращает
        код ответа 400 и что количество объектов модели File равно 0, то есть
        объект не создан.
        """
        invalid_data = {'invalid': 'text'}
        response = self.client.post(
            '/api/upload/',
            invalid_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(File.objects.count(), 0)

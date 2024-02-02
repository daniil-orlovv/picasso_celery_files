from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from files.models import File
from api.tasks import update_processed_field


# Попытка покрыть тестами Celery...
class CeleryTaskTest(TestCase):
    def test_update_processed_field_task(self):
        file_content = b'Text.'
        uploaded_file = SimpleUploadedFile("testfile.txt", file_content)
        file_instance = File.objects.create(file=uploaded_file)

        update_processed_field.delay(file_instance.id, True)

        updated_file_instance = File.objects.get(id=file_instance.id)

        self.assertTrue(updated_file_instance.processed)

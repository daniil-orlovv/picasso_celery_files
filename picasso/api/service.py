from files.models import File


def update(file_id, new_value):
    file_obj = File.objects.get(pk=file_id)
    print(f"Updating processed field for file_id {file_id} to {new_value}")
    file_obj.processed = new_value
    file_obj.save()
    return f"Значение поля файла успешно обновлено: {file_obj}"

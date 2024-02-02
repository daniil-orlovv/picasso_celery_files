from django.contrib import admin

from files.models import File


class FileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'file',
        'uploaded_at',
        'processed'
    )


admin.site.register(File, FileAdmin)

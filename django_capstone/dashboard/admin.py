from django.contrib import admin

# Register your models here.
from .models import UploadOptionModel, Video

admin.site.register(UploadOptionModel)
admin.site.register(Video)

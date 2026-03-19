from django.contrib import admin

from dds import models


admin.site.register(models.DDSType)
admin.site.register(models.DDSSubcategory)
admin.site.register(models.DDSCategory)
admin.site.register(models.DDSEntry)
admin.site.register(models.DDSStatus)

from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.ServiceProvider)
admin.site.register(models.Range)
admin.site.register(models.Chat)
admin.site.register(models.Message)
admin.site.register(models.Order)
admin.site.register(models.Review)
admin.site.register(models.Location)


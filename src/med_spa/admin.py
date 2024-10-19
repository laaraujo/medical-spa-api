from django.contrib import admin

from med_spa import models

admin.site.register(models.MedicalSpa)
admin.site.register(models.ServiceProductProvider)
admin.site.register(models.ServiceCategory)
admin.site.register(models.ServiceType)
admin.site.register(models.ServiceProduct)
admin.site.register(models.Service)
admin.site.register(models.Appointment)

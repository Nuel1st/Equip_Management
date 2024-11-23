from django.contrib import admin
from .models import Equipment, Surveyor, Equipment_Request


# admin.site.register(Equipment)
admin.site.register(Surveyor)
admin.site.register(Equipment_Request)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment_type', 'status')
from django.contrib import admin
from .models import Patient, Attachment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id","nombre","dni","cobertura","medico","sector_code","estado","fecha_cx","created_at")
    list_filter = ("sector_code","estado","cobertura","medico")
    search_fields = ("nombre","dni","cobertura","medico")

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id","patient","kind","file","created_at")
    list_filter = ("kind",)
    search_fields = ("patient__nombre","patient__dni")

from django.contrib import admin

# Register your models here.
from apps.tasques.models import Tasca , Aplicacio, Estat
 
admin.site.register(Tasca)
admin.site.register(Aplicacio)
admin.site.register(Estat)
##class EstatAdmin(admin.ModelAdmin):
##    list_display = ("nom", "color")
##    list_editable = ("color",)
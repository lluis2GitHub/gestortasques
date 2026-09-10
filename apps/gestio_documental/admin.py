from django.contrib import admin
from .models import Document, DocumentVersion


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'tipus_mime', 'mida_bytes',
                    'etiqueta', 'creat_per', 'creat')
    search_fields = ('nom', 'descripcio', 'etiqueta')
    list_filter = ('tipus_mime', 'etiqueta', 'creat_per')


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'versio', 'creat', 'creat_per')
    list_filter = ('document',)

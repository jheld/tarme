from django.contrib import admin
from compression.models import Document, CompressedDocument

class DocumentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Document, DocumentAdmin)


class CompressedDocumentAdmin(admin.ModelAdmin):
    pass
admin.site.register(CompressedDocument, CompressedDocumentAdmin)

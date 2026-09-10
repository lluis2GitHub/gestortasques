from django.db import models
from .models import Document

class DocumentableMixin(models.Model):
    """
    Qualsevol model que hereti d’això pot tenir documents associats.
    """

    documents = models.ManyToManyField(
        Document,
        blank=True,
        related_name='objectes_relacionats'
    )

    class Meta:
        abstract = True
    
    def add_document(self, file, title=None, description=None, user=None):
        doc = Document.objects.create(
            nom=title or file.name,
            fitxer=file,
            descripcio=description or "",
            creat_per=user
        )
        self.documents.add(doc)
        return doc


    def remove_document(self, document_id):
        """
        Elimina l’associació i opcionalment el document.
        """
        try:
            doc = self.documents.get(id=document_id)
            self.documents.remove(doc)
            doc.delete()
        except Document.DoesNotExist:
            pass

    def get_documents(self):
        """
        Retorna tots els documents associats.
        """
        return self.documents.all()

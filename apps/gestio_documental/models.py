from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Document(models.Model):
    nom = models.CharField(max_length=255)
    fitxer = models.FileField(upload_to='gestio_documental/docs/')
    tipus_mime = models.CharField(max_length=100, blank=True)
    mida_bytes = models.PositiveIntegerField(null=True, blank=True)

    descripcio = models.TextField(blank=True)
    etiqueta = models.CharField(max_length=50, blank=True)

    creat_per = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='documents_creats'
    )
    creat = models.DateTimeField(auto_now_add=True)
    modificat = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creat']

    def __str__(self):
        return self.nom


class DocumentVersion(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    fitxer = models.FileField(upload_to='documents/versions/')
    versio = models.PositiveIntegerField()
    creat = models.DateTimeField(auto_now_add=True)
    creat_per = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='versions_creades'
    )

    class Meta:
        unique_together = ('document', 'versio')
        ordering = ['-versio']

    def __str__(self):
        return f'{self.document.nom} v{self.versio}'

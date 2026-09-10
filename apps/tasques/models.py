from django.db import models
from django.contrib.auth.models import User
from schedule.models import Calendar, Event
from apps.gestio_documental.mixins import DocumentableMixin

class Estat(models.Model): 
    nom = models.CharField(max_length=100) 
    color = models.CharField(max_length=7, default="#6c757d")  # format #RRGGBB
    def __str__(self): 
        return self.nom 
    
# Create your models here.
class Aplicacio(models.Model): 
    nom = models.CharField(max_length=100) 
    def __str__(self): 
        return self.nom 
 
 
class Tasca(models.Model): 
 
    PRIORITATS = [ 
        ('baixa', 'Baixa'), 
        ('mitjana', 'Mitjana'), 
        ('alta', 'Alta'), 
        ('critica', 'Crítica'), 
    ] 
 
    titol = models.CharField(max_length=200) 
    descripcio = models.TextField(blank=True) 
    completada = models.BooleanField(default=False) 
    data_creacio = models.DateTimeField(auto_now_add=True) 
 
    data_inici = models.DateTimeField()
    data_fi_prevista = models.DateTimeField()
    prioritat = models.CharField(max_length=10, choices=PRIORITATS, default='mitjana') 
    aplicacio = models.ForeignKey(Aplicacio, on_delete=models.SET_NULL, null=True, blank=True) 
    estat = models.ForeignKey(Estat, on_delete=models.SET_NULL, null=True, blank=True) 
    usuari = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Calendari únic per a totes les tasques
        calendar, _ = Calendar.objects.get_or_create(
            slug="tasques",
            defaults={"name": "Tasques"}
        )

        # Identificador estable per a l'Event
        event_title = f"Tasca-{self.id}"

        # Crear o actualitzar l'esdeveniment
        Event.objects.update_or_create(
            calendar=calendar,
            title=event_title,
            defaults={
                "start": self.data_inici,
                "end": self.data_fi_prevista,
                "description": self.descripcio,
            }
        )

    def __str__(self): 
        return self.titol 
    

class Nota(DocumentableMixin, models.Model):
    tasca = models.ForeignKey(
        Tasca,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    text = models.TextField()
    creat_el = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creat_el']  # De més nova a més antiga

    def __str__(self):
        return f"Nota {self.id} per {self.tasca.titol}"
    
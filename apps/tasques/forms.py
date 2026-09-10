from django import forms
from django.forms import DateTimeInput
from .models import Tasca, Nota
from django.utils import timezone
from apps.gestio_documental.forms import DocumentForm

class TascaForm(forms.ModelForm): 
    class Meta: 
        model = Tasca 
        fields = [ 
            'titol', 'descripcio', 'completada', 
            'data_inici', 'data_fi_prevista', 
            'prioritat', 'aplicacio', 'estat'
        ] 
        widgets = {
            "data_inici": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"}
            ),
            "data_fi_prevista": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"}
            ),
        }
        input_formats = {
            "data_inici": ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S"],
            "data_fi_prevista": ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S"],
        }

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
        }
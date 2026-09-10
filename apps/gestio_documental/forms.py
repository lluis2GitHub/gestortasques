from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['nom', 'fitxer', 'descripcio', 'etiqueta']
        widgets = {
            "fitxer": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "descripcio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
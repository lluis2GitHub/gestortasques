from django import template

register = template.Library()

#@register.filter(name='add_class')
#def add_class(field, css):
#    return field.as_widget(attrs={"class": css})
#    return field.as_widget(attrs={**field.field.widget.attrs, "class": css})

# @register.filter(name='add_class')
# def add_class(field, css):
#     # Recupera els atributs existents del widget
#     attrs = field.field.widget.attrs.copy()

#     # Afegeix la classe sense eliminar la resta
#     existing = attrs.get("class", "")
#     attrs["class"] = f"{existing} {css}".strip()

#     # Renderitza el widget amb tots els atributs intactes
#     return field.as_widget(attrs=attrs)

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})
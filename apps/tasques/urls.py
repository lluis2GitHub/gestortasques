from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views 
from .calendar_views import calendar_month_view, calendar_week_view, calendar_day_view, view_gantt

app_name = "tasques"

urlpatterns = [ 
   path('', views.llista_tasques, name='llista_tasques'), 
   path('eliminar/<int:pk>/', views.eliminar_tasca, name='eliminar_tasca'),
   path("tasques/nova/", views.crear_tasca, name="crear_tasca"),
   path("tasques/<int:pk>/editar/", views.editar_tasca, name="editar_tasca"),
   path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
   path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
   path('notes/<int:pk>/editar/', views.editar_nota, name='editar_nota'),
   path('notes/<int:pk>/eliminar/', views.eliminar_nota, name='eliminar_nota'),
   path("calendari/mes/", calendar_month_view, name="calendari_mes"),
   path("calendari/setmana/", calendar_week_view, name="calendari_setmana"),
   path("calendari/dia/", calendar_day_view, name="calendari_dia"),
   path("gantt/", view_gantt, name="gantt"),
   path("nota/<int:nota_id>/document/", views.afegir_document, name="afegir_document"),
   path("nota/<int:nota_id>/documents/", views.documents_nota, name="documents_nota"),
   path("document/eliminar/<int:pk>/", views.eliminar_document, name="eliminar_document"),

]  
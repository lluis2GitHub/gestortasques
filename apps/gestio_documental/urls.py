from django.urls import path
from . import views


app_name = 'gestio_documental'

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('nou/', views.document_create, name='document_create'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
] 

from django.urls import path
from . import views

app_name = 'esia'
urlpatterns = [
    path('', views.index, name='index'),
    path('esia/', views.callback, name='callback')
]
from django.urls import path
from . import views

app_name = 'about'
urlpatterns = [
    path('', views.dashboard, name='index'),
    path('dashboard/', views.dashboard, name='dashboard')
]
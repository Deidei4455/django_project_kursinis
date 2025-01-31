from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_n'),
    path('paslaugos/', views.paslaugos, name='paslaugos_n')
]

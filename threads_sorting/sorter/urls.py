from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/status/', views.status_api, name='status_api'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('api/v1/', views.web_api_v1, name='web_api_v1'),
]

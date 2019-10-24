from django.urls import path

from . import views

urlpatterns = [
    path('', views.web_01, name='web_01'),
    path('web_01/', views.web_01, name='web_01'),
    path('web_02/', views.web_02, name='web_02'),
]

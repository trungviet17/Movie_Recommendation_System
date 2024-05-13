from django.urls import path 
from . import views


app_name = 'main'


urlpatterns = [
    path('', views.home, name='home'), 
    path('similarity/', views.similarity, name='similarity'),
    path('recommend/', views.recommend, name='recommend'),
]
from django.urls import path 
from . import views


app_name = 'main'


urlpatterns = [
    path('', views.home, name='home'), 
    path('search/', views.search, name='search'), 
    path('recommend/<int:movie_id>/', views.recommend, name='recommend'),
]
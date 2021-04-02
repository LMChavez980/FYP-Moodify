from django.urls import path
from moodyapi import views

urlpatterns = [
    path('', views.index_page),
    path('analyze', views.analyze_playlist),
    path('generate', views.generate_playlist),
    path('statistics', views.mood_statistics)
]
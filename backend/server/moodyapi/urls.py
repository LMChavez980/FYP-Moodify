from django.urls import path
from moodyapi import views

urlpatterns = [
    #path('',views.index_page),
    path('analyze', views.AnalyzeView.as_view())
]
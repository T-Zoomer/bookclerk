from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('get-recommendations/', views.get_recommendations, name='get_recommendations'),
    path('recommendations/<uuid:request_id>/', views.view_recommendations, name='view_recommendations'),
]
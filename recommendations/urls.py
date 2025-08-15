from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-recommendations/', views.get_recommendations, name='get_recommendations'),
    path('recommendations/<int:request_id>/', views.view_recommendations, name='view_recommendations'),
]
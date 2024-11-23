from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Default homepage route
    path('request-equipment/', views.equipment_request, name='equipment_request'),
    path('get-equipment-dropdown/', views.get_equipment_dropdown, name='get_equipment_dropdown'),
    # path('request-success/', views.request_success, name='request_success'),
]
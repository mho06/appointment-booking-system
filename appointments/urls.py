from django.contrib import admin
from . import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)


urlpatterns = [
    path('book/', views.appointment_form, name='appointment_form'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('api/', include(router.urls)),
    
]
from django.contrib import admin
from django.urls import path, include
from appointments import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Appointment booking
    path('', views.appointment_form, name='appointment_form'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('appointments/<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),

    # Django REST Framework browsable API (optional)
    path('api/', include('rest_framework.urls')),
]

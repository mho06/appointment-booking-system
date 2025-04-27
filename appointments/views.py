from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Appointment
from .forms import AppointmentForm, SignUpForm
from .serializers import AppointmentSerializer

# Django Rest Framework ViewSet
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

# User signup
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('appointment_form')
    else:
        form = SignUpForm()
    return render(request, 'appointments/signup.html', {'form': form})

# User login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request, 
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome back!')
                return redirect('appointment_form')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'appointments/login.html', {'form': form})

# User logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Book an appointment (Home page)
@login_required
def appointment_form(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointment_list')
        else:
            messages.error(request, 'Error in form. Try again.')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form})

# List all appointments
@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

# Edit an appointment
@login_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/appointment_edit.html', {'form': form})

# Delete an appointment
@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == "POST":
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})

# Cancel appointment (set status to Canceled)
@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    appointment.status = 'Canceled'
    appointment.save()
    messages.success(request, 'Appointment canceled successfully.')
    return redirect('appointment_list')

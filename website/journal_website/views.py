from django.shortcuts import render, redirect
from .forms import RegistrationForm

def display_home_page(request):
    return render(request, 'home.html')

def register_user(request):
    error_message = ''

    if request.method == 'POST':
        data_from_form = RegistrationForm(request.POST)
        if data_from_form.is_valid():
            data_from_form.save()
            return redirect('home')
        else:
            error_message = 'Form is invalid'

    registration_form = RegistrationForm()
    data_to_show_in_template = {
        'form': registration_form,
        'error': error_message
    }
    return render(request, 'authorization/registration.html', data_to_show_in_template)
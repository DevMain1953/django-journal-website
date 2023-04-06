from django.shortcuts import render
from .repositories import UserRepository

user_repositpry = UserRepository.UserRepository()

def display_main_page(request):
    return render(request, 'main.html')

def display_registration_page(request):
    return render(request, 'authorization/registration.html')

def create_user(request):
    if request.method == 'POST':
        user_repositpry.create_user(first_name=request.POST['first_name'],
                                    second_name=request.POST['second_name'],
                                    middle_name=request.POST['middle_name'],
                                    email=request.POST['email'],
                                    nickname=request.POST['nickname'],
                                    password=request.POST['password'])
    display_main_page()
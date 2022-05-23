from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile
from .forms import UserForm,ProfileForm,WeatherForm
import requests
import os
from dotenv import load_dotenv
load_dotenv()
@login_required
def Home(request):
    location = request.GET.get('location')
    api_key = str(os.getenv('OPENWEATHERMAP_API_KEY'))
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': location, 'appid': api_key, 'pretty': 1}
    weather_form = WeatherForm()
    if(location):
        r = requests.get(url, params=params)
        locations = r.json()
        return render(request, 'home.html', {'weather_form': weather_form, 'locations': locations})
    else:
        locations = {}
        return render(request, 'home.html', {'weather_form': weather_form, 'locations': locations})
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import requests
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'users/index.html')


def login(request):
    return render(request, 'users/login.html')


def logout(request):
    return render(request, 'users/logout.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form.cleaned_data.get("username")
            messages.success(request, f'Your account has been created, please Log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def youtube(request):
    thumbnails = []
    titles = []
    context = []
    if request.method == "POST":
        channel_name = request.POST.get('fname')
        print(channel_name)
        search_url = 'https://www.googleapis.com/youtube/v3/search'

        params = {
            'part': 'snippet',
            'type': 'channel',
            'q': channel_name,
            'key': settings.YOUTUBE_DATA_API_KEY,
        }

        res_channel = requests.get(search_url, params=params)
        print(res_channel.text)
        channel_id = res_channel.json()['items'][0]['id']['channelId']
        playlist_url = 'https://www.googleapis.com/youtube/v3/search'
        params_playlist = {
            'part': 'snippet',
            'channelId': channel_id,
            'key': settings.YOUTUBE_DATA_API_KEY,
            'order': 'date',
            'maxResults': 10,

        }
        res_videos = requests.get(playlist_url, params=params_playlist)

        for i in range(10):
            titles.append(res_videos.json()['items'][i]['snippet']['title'])
            thumbnails.append(res_videos.json()['items'][i]['snippet']['thumbnails']['medium']['url'])
        context = zip(thumbnails, titles)
    return render(request, 'users/youtube.html', {'context': context})

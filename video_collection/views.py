from django.shortcuts import render, redirect
from .models import Video
from .forms import VideoForm, SearchForm
from django.contrib import messages 
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower

# Create your views here.
#create homepage view here

def home(request):
    app_name = 'Most Watched Videos' #name for my videos 
    return render(request, 'video_collection/home.html', {'app_name': app_name})


def add(request):
    if request.method == 'POST':   # adding a new video
        new_video_form = VideoForm(request.POST) 
        if new_video_form.is_valid():  #is the form valid ???
            try:
                new_video_form.save()  # Creates new Video object and saves 
                return redirect('video_list')#no message sent to user
            except IntegrityError:
                messages.warning(request, 'You already added that video') #user message
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')##user message 
        
        # Invalid form 
        messages.warning(request, 'Check the data entered')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form}) 
            
        
    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form}) 
    

def video_list(request):

    search_form = SearchForm(request.GET)  #build the form from data user has sent to app

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name')) #sorting the order

    else:  #form is not filled in or the first time the user sees the page
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name')) 

    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})




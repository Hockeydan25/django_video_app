from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .forms import VideoForm
from .models import Video


"""
Create your views here.
"""

def home(request):
    app_name = 'Music Videos'  # video collection name created with be used in place holder app.name on home page.
    return render(request, 'video_collection/home.html', {'app_name': app_name})  # key and value

def add(request):
    if request.method == 'POST':  # adding a new video
        new_video_form = VideoForm(request.POST)  # what is this?
        if new_video_form.is_valid():
            try:
                new_video_form.save()  # saves creates video object that contains the video url?
                return redirect('video_catelog')
                #messages.info(request, 'New video was saved!')
                # todo show sucess or redirect to list of videos
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError:
                messages.warning(request, 'You already adding this video!')        
        
        messages.warning(request, 'Please check that you enter data all in the fields.')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})  


    new_video_form = VideoForm() # this is going to use forms for our new video so when you add it you can fill out.   
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

def video_catelog(request):  # video catelog used instead of video_list, function
    videos = Video.objects.all()
    return render(request, 'video_collection/video_catelog.html', {'videos': videos})

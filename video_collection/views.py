from django.shortcuts import render
from .models import Video
from .forms import VideoForm
from django.contrib import messages


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
            new_video_form.save()  # saves creates video object that contains the video url?
            messages.info(request, 'New video was saved!')
            # todo show sucess or redirect to list of videos
        else:
            messages.warning(request, 'Please check that you enter data all in the fields.')
            return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})  


    new_video_form = VideoForm() # this is going to use forms for our new video so when you add it you can fill out.   
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})
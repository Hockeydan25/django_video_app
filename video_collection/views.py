from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from .forms import SearchFrom, VideoForm
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
                return redirect('video_catalog')
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

def video_catalog(request):  # video catelog used instead of video_list, function

    search_form = SearchFrom(request.GET)  # build form from data use has sent to the app

    if search_form.is_valid():
        print(search_form)
        search_term = search_form.cleaned_data['search_term']  # user sent data music video 'soundgarden' or 'jon spencer'
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name'))  # add sorting lower order

    else:  # fomr is not valid in or this is the first time the user sees the page.
        search_form = SearchFrom()  # calls the method from forms
        videos = Video.objects.order_by(Lower('name'))  # add sorting lower order

    return render(request, 'video_collection/video_catalog.html', {'videos': videos, 'search_form': search_form})
 
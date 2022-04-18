from django.urls import path
from . import views

'''
each page needs URL, View and Template for the home page. 
don't forget comma's we adding paths.
'''

urlpatterns = [    
    path('', views.home, name='home'),
    path('add', views.add, name='add_video' ),  # will end up with a button, submit type
    path('video_catalog', views.video_catalog, name='video_catalog' )  # using category instead of list. 
]

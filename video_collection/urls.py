from django.urls import path
from . import views

'''
every page needs URL, View and Template for the home page. 
don't forget comma's we adding paths.
'''

urlpatterns = [    
    path('', views.home, name='home'),
    path('add', views.add, name='add_video' )  # will end up with a button, submitt type
]

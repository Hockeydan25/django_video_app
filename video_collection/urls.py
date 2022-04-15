from django.urls import path
from . import views

'''
every page needs URL, View and Template for the home page.
'''

urlpatterns = [
    path('', views.home, name='home')
]

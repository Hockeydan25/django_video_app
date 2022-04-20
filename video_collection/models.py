from urllib import parse
from django.db import models
from django.forms import ValidationError

""" 
Create your models here. name, url(youtube only), notes, add video button and some links.
don't for get about migrations when creating new models to add in the table to the database with it's constriants. 
"""

class Video(models.Model):  # superclass 
    name = models.CharField(max_length=250)  # database constriants
    url = models.CharField(max_length=400)  # longer for urls they can be lengthy.
    notes = models.TextField(blank=True, null=True)  # blank notes are optional so True, allows null value
    video_id = models.CharField(max_length=40, unique=True)


    def save(self, *args, **kwargs):  # save function. args arguments, kwargs key word arguments.

        # extracts the video id from a youtube url does not gaurentee.
        # if not self.url.startswith('https://www.youtube.com/watch'):
        #     raise ValidationError(f'Hi, check your URL link, please use a YouTube URL {self.url}')
        url_components = parse.urlparse(self.url)

        #new validation checks 
        if url_components.scheme != 'https':
            raise ValidationError(f'Hi, check your URL link, please use a YouTube URL {self.url}')

        if url_components.netloc != 'www.youtube.com':
            raise ValidationError(f'Hi, check your URL link, please use a YouTube URL {self.url}')

        if url_components.path != '/watch':
            raise ValidationError(f'Hi, check your URL link, please use a YouTube URL {self.url}')    


        query_string = url_components.query  # the v is in a youtube video 'v=10988776'/ a list.   
        if not query_string:
            raise ValidationError('Invalid YouTube URL {self.url}')  # dictionary format.
        parameters = parse.parse_qs(query_string,  strict_parsing=True)  # database sqlite command.
        v_paramters_catelog = parameters.get('v')  # return None if no key found, ie.. abc=1234. we need to deal with None.
        if not v_paramters_catelog:  # check for None or empty list.
            raise ValidationError(f'Invalida YouTube URL, missing parameters {self.url}') 
        self.video_id =v_paramters_catelog[0]  #string v.

        super().save(*args, **kwargs)  
        # superclass save function calling the model.Model method - overwrites save function with Models save().


    def __str__(self) -> str:  
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id} ,Notes: {self.notes[:200]}'  # notes limited[:200] 



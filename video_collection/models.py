from django.db import models

""" 
Create your models here. name, url(youtube only), notes, add video button and some links.
don't for get about migrations when creating new models to add in the table to the database with it's constriants. 
"""

class Video(models.Model):
    name = models.CharField(max_length=250)  # database constriants
    url = models.CharField(max_length=400)  # longer for urls they can be lengthy.
    notes = models.TextField(blank=True, null=True)  # blank notes are optional so True, allows null value
    # creates string on page 
    def __str__(self) -> str:  
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Notes: {self.notes[:200]}'  # notes limited[:200] 



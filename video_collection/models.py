from django.db import models

# Create your models here.
#video table 
class Video(models.Model):
    name = models.CharField(max_length=200) #required user input
    url = models.CharField(max_length=400) #required user input 
    notes = models.TextField(blank=True, null=True)  #notes feild to be optional in the form 


    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Notes: {self.notes[:200]}'#tuncate to first 200 characters in user notes

from urllib import parse #errors if not put first???

from django.db import models

from django.core.exceptions import ValidationError  #will error lines 21, 25


# Create your models here.
#video table 
class Video(models.Model):
    name = models.CharField(max_length=200) #required user input
    url = models.CharField(max_length=400) #required user input 
    notes = models.TextField(blank=True, null=True)  #notes feild to be optional in the form 
    video_id = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        #extract video ID from a youtube URL

        # if not self.url.startswith('https://www.youtube.com/watch'):
        #     raise ValidationError(f'Not a Youtube UR {self.url}L')

        url_components = parse.urlparse(self.url) #known in python to save
        query_string = url_components.query
        if not query_string:
            raise ValidationError(f'Invalid youtube URL {self.url}')
        
        if url_components.scheme != 'https':
            raise ValidationError(f'Not a YouTube URL {self.url} ')

        if url_components.netloc != 'www.youtube.com':  #short for network location 
            raise ValidationError(f'Not a YouTube URL {self.url} ')

        if url_components.path != '/watch':
            raise ValidationError(f'Not a YouTube URL {self.url} ')


        parameters = parse.parse_qs(query_string, strict_parsing=True) #dictionary
        v_parameters_list = parameters.get('v') #returns none if no key found
        if not v_parameters_list:    #check if NONE or empty list
            raise ValidationError(f'Missing Parameters {self.url}')
        self.video_id = v_parameters_list[0]  #string 

        super().save(*args, **kwargs)


    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id}, Notes: {self.notes[:200]}'#tuncate to first 200 characters in user notes

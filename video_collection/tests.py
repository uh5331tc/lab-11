from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse  #convert a name of a URL into a path for the server
from .models import Video
from django.core.exceptions import ValidationError
# Create your tests here.

class TestHomePageMessage(TestCase):
    def test_app_tittle_message_shown_on_home_page(self):
        url = reverse('home')
        response = self.client.get(url) 
        self.assertContains(response, 'My Favorite Vidoes')


class TestAddVideos(TestCase):
    def test_add_video(self):
        valid_video = {
            'name': 'yoga',
            'url': 'https://www.youtube.com/watch?v=4vTJHUDB5ak',
            'notes': 'notes are cool'
        }

        url = reverse('add_video')
        response = self.client.post(url, data=valid_video, follow=True)  #expects a dictionary 

        self.assertTemplateUsed('video_collection/video_list.html')
        

        #does the video list show the new video?
        self.assertContains(response, 'yoga')
        self.assertContains(response, 'yoga for legs')
        self.assertContains(response, 'https://www.youtube.com/watch?v=4vTJHUDB5ak')

        video_count = Video.objects.count()
        self.assertEqual(1, video_count)

        video = Video.objects.first()
        self.assertEqual('yoga', video.name)
        self.assertEqual('https://www.youtube.com/watch?v=4vTJHUDB5ak', video.url)
        self.assertEqual('yoga for legs', video.notes)
        self.assertEqual('4vTJHUDB5ak', video.video_id)


    def test_add_video_invalid_url_not_added(self):

        invalid_video_urls = [
            'https://www.youtube.com',
            'https://www.youtube.com/watch?v=as;lkdfj',
            '',
            'https://www.github.com'
        ]

        for invalid_video_url in invalid_video_urls:
            new_video = {
                'name': 'example',
                'url': invalid_video_url,
                'notes': 'exapmple notes'
            }

            url = response('add_video')
            response = self.client.post(url, new_video)

            self.assertTemplateUsed('video_collection/add.html')

            messages = response.context('messages')
            message_texts = [ message.message for message in messages]

            self.assertIn('Invalid YouTube URL', message_texts)  #checking 
            self.assertIn('Please check the data entered.', message_texts)  #checking 

            video_count = Video.objects.count()
            self.assertEqual(0, video_count)

class TestVideoList(TestCase):
    def test_all_videos_displayed_in_correct_order(self):
        v1 = Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=4vTJHUDB5ak')
        v2 = Video.objects.create(name='ABC', notes='example', url='https://www.youtube.com/watch?v=weeJHUDB5ak')
        v3 = Video.objects.create(name='ACAB', notes='example', url='https://www.youtube.com/watch?v=w33HUDB5ak')
        v4 = Video.objects.create(name='BACA', notes='example', url='https://www.youtube.com/watch?v=wLLLJHUDB5ak')

#checks to see if they are ordered in a case-sensitive way
        expected_order = [v1, v2, v3, v4]

        url = reverse('video_list')
        response = self.client.get(url)

        videos_in_template = list(response.context['videos'])

        self.assertEqual(videos_in_template, expected_order)

        def test_no_video_message(self):  #no video message
            url = reverse('video_list')
            response = self.client.get(url)
            videos_in_template = response.context['videos']
            self.assertContains(response, 'No videos.')
            self.assertEquals(0, len(response.context['videos']))

        def test_video_number_message_two_video(self):
            v1 = Video.objects.create(name='ZYX', notes='exapmple', url='https://www.youtube.com/watch?v=4vTJHUDB5ak')
            v2 = Video.objects.create(name='ZYK', notes='exape', url='https://www.youtube.com/watch?v=4vTJHUDB6lk')
            
            url = reverse('video_list')
            response = self.client.get(url)

            self.assertContains(response, '1 video')  #corect 
            self.assertNotContaints(response, '2 videos') #not correct





class TestVideoSearch(TestCase):
    pass 

class TestVideoModel(TestCase):

    def test_invalid_url_raises_validation_error(self):
        invalid_video_urls = [
            'https://www.youtube.com',
            'https://www.youtube.com/watch?v=as;lkdfj',
            '',
            'https://www.github.com'
        ]

        for invalid_video_url in invalid_video_urls:

            with self.assertRaises(ValidationError):

                video = {
                    'name': 'example',
                    'url': invalid_video_url,
                    'notes': 'exapmple notes'
                }
                
                Video.objects.create(name='example',  url='invalid_video_url', notes='exapmple notes')
            self.assertEqual(0, Video.objects.count())

    def test_duplicate_video_raises_integrity_error(self):
        v2 = Video.objects.create(name='ZYK', notes='exape', url='https://www.youtube.com/watch?v=4vTJHUDB6lk')
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='ZYK', notes='exape', url='https://www.youtube.com/watch?v=4vTJHUDB6lk')

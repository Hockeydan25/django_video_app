from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Video

'''
reverse wil convert the name of the url into an actual path.

'''

class TestHomePageMessage(TestCase):

    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Music Videos')

class TestAddVideos(TestCase):
    
    def test_add_video(self):  # Adding a video, added to DB and video_id created. 

        valid_video = {
            'name': 'Jon Spencer',
            'url': 'https://www.youtube.com/watch?v=IWY4gmbOz24',
            'notes': 'Song Worm Town'
        }
        url = reverse('add_video')
        response = self.client.post(url, data=valid_video, follow=True)  # follow will allow redirect to the youtube page to not error.

        self.assertTemplateUsed('video_collection/video_catalog.html')
        # does the video catelog show the new video
        self.assertContains(response, 'Jon Spencer' )
        self.assertContains(response, 'Song Worm Town')
        self.assertContains(response, 'https://www.youtube.com/watch?v=IWY4gmbOz24')

        video_count= Video.objects.count()
        self.assertEqual(1, video_count)  # checking database is getting added.

        video = Video.objects.first()

        self.assertEqual( 'Jon Spencer', video.name)
        self.assertEqual( 'Song Worm Town', video.notes)
        self.assertEqual( 'https://www.youtube.com/watch?v=IWY4gmbOz24', video.url)
        self.assertEqual( 'IWY4gmbOz24', video.video_id)


    def test_add_video_invalid_urls_not_added(self):

        invalid_video_urls = [
            'https://www.youtube.com/'
            'https://www.youtube.com/watch?'
            'https://www.youtube.com/watch?abc123'
            'https://www.youtube.com/watch?v='
            'https://www.youtube.com/watch'
            'https://minneapolis.edu'
            'https://minneapolis.edu?v=098786'
        ]
        for  invalid_video_url in  invalid_video_urls:

            new_video = {
                'name': 'example',
                'url':  invalid_video_url,
                'notes': 'example note'
            }
            url = reverse('add_video')
            response = self.client.post(url, new_video)

            self.assertTemplateNotUsed('video_collection/add.html')

            messages = response.context['messages']
            message_texts = [ message.message for message in messages]

            self.assertIn('Invalid YouTube URL', message_texts)
            self.assertIn('Please check that you enter data all in the fields.', message_texts)

        video_count= Video.objects.count()
        self.assertEqual(0, video_count)  # checking database is mot getting added to.

        
class TestVideoCatelog(TestCase):    

    def test_all_videos_displayed_in_correct_order(self):

        v1 =Video.objects.create(name='ZYX', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 =Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=124')
        v3 =Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=125')
        v4 =Video.objects.create(name='lmn', notes='example', url='https://www.youtube.com/watch?v=126')
    
        expected_video_order = [v3,v2,v4,v1]  # simply list in order expected

        url = reverse('video_catalog')
        response = self.client.get(url)

        videos_in_template = list(response.context['videos'])

        self.assertEqual(videos_in_template, expected_video_order)

    def test_no_video_message(self):
        url = reverse('video_catalog')
        response = self.client.get(url)
        self.assertContains(response, 'No Videos')  # must match, same as empty in HTML template
        self.assertEqual(0, len(response.context['videos']))    


    def test_one_video_number_message_one_video(self):
        v1 =Video.objects.create(name='ZYX', notes='example', url='https://www.youtube.com/watch?v=123')
        url = reverse('video_catalog')
        response = self.client.get(url)

        self.assertContains(response, '1 video') 
        self.assertNotContains(response, '1 videos') 

    
    def test_video_number_message_two_video(self):
        v1 =Video.objects.create(name='ZYX', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 =Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=124')
        url = reverse('video_catalog')
        response = self.client.get(url)

        self.assertContains(response, '2 videos') 
    
    


class TestVideoSearch(TestCase):

    pass

class TestVideoMode(TestCase):


    def test_invalid_url_raises_validation_error(self):
        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch/somethingelse',
            'https://www.youtube.com/watch/somethingelse?v=1234567',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?abc=123',
            'https://www.youtube.com/watch?v=',
            'https://github.com',
            '12345678',
            'htttttttttps://www.youtube.com/watch',
            'http://www.youtube.com/watch/somethingelse?v=1234567',
            'https://minneapolis.edu',
            'https://minneapolis.edu?v=123456'
        ]

        for  invalid_video_url in  invalid_video_urls:             
            with self.assertRaises(ValidationError):
                Video.objects.create(name='example', url=invalid_video_url, notes='example note')

        self.assertEqual(0, Video.objects.count())


    def test_duplicate_video_raises_intgrety_error(self):
        v1 =Video.objects.create(name='ZYX', notes='example', url='https://www.youtube.com/watch?v=123')
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='ZYX', notes='example', url='https://www.youtube.com/watch?v=123')


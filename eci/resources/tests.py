from django.test import TestCase, Client
from django.core import urlresolvers
from django.contrib.auth import SESSION_KEY
import httplib

class NewUserTestCase(TestCase):
    #assert the new users come not authenticated to our site
    def setUp(self):
        self.client = Client()
        logged_in = self.client.session.has_key(SESSION_KEY)
        self.assertFalse(logged_in)
    #new user enter first time in our site
    def test_view_homepage(self):
        client = Client()
        home_url = urlresolvers.reverse('home')
        response = client.get(home_url)
        #check that we did get a response
        self.failUnless(response)
        #check that the status code was a SUCCES ( httplib.OK =200 )
        self.assertEqual(response.status_code,httplib.OK)
        
    def test_view_login_required_page(self):
        client = Client()
        home_url = urlresolvers.reverse('resources_subjects')
        response = client.get(home_url)
        #check that we did get a response
        self.failUnless(response)
        #check that the status code was FOUND ( httplib.OK =302)
        #and the user was redirected
        self.assertEqual(response.status_code,httplib.FOUND)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

try:
    import json
except ImportError:
    import simplejson
    
import base64
import random

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from pymongo import Connection

class HttpApiTest(TestCase):  

    """
    
    You must 
    
    Django client cheat sheet:
    
    Client methods:
    
        get(path, data={}, follow=False) 
        post(path, data={}, follow=False) 
        head(path, data={}, follow=False)
        options(path, data={}, follow=False) 
        put(path, data={}, follow=False) 
        delete(path, data={}, follow=False) 
        login(options) 
        logout() 
    
    Reponse attributes:
       
        client 
        content 
        context 
        request 
        status_code
        template  
    
    """
    
    fixtures = ['features_test.json']
    
    def __init__(self, *args, **kwargs):
    
        # settings up HTTP authentification credentials
        
        try:
            username = settings.HTTP_TEST_USERNAME
            password = settings.HTTP_TEST_PASSWORD
        except AttributeError:
            raise Exception('You must define settings.HTTP_TEST_USERNAME '\
                            'and settings.HTTP_TEST_USERNAME to be able to '\
                            'test HTTP authentification')
        if not authenticate(username=username, password=password):
            raise Exception('settings.HTTP_TEST_USERNAME and '\
                            'settings.HTTP_TEST_PASSWORD are not valid '\
                            'credentials. Could not login.')
        
        auth = 'Basic %s' % base64.encodestring('%s:%s' % (username, password))
        self.auth = {'HTTP_AUTHORIZATION': auth.strip()}
        TestCase.__init__(self, *args, **kwargs)
    
    
    def assertJsonMatchDict(self, url, d, code):
        response = self.client.get(url, **self.auth) 
        self.assertEqual(d, json.loads(response.content))
        self.failUnlessEqual(str(response.status_code), str(code)) 


    def assertPageMatch(self, url, content, code='200'):
        response = self.client.get(url, **self.auth)
        self.assertTrue(content in response.content)
        self.assertEqual(str(response.status_code), str(code))
    
    
    def create_test_feature(self, name='test'):
        url = '/api/v1/createfeature/'
        coord = "[%s, %s]" % (random.random() * 10, random.random() * 10)
        response = self.client.post(url, {
                                    "subdivision_code": "FR",
                                    "country_code": "FR",
                                    "feature_type": "school",
                                    "geometry_type": "Point",
                                    "geometry_coordinates": coord,
                                    "name": name}, **self.auth) 
        return response
    
    
    def setUp(self):     
    
        self.client = Client()
    
        # set up mongo
        self.con = Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        self.db = self.con[settings.MONGO_DB_NAME]
        self.transactions = self.db[settings.MONGO_DB_NAME]
        self.history = self.db[settings.MONGO_HISTORYDB_NAME]
        
        # set up a test user
        self.user, created = User.objects.get_or_create(username=settings.HTTP_TEST_USERNAME)
        self.user.set_password(settings.HTTP_TEST_PASSWORD)
        self.user.save()
        
     
    def tearDown(self):
        self.con.drop_database(settings.MONGO_DB_NAME)
        self.con.disconnect()


    def test_view_unknown_page(self):     
        response = self.client.get('/nothing/', {}, **self.auth)     
        self.failUnlessEqual(response.status_code, 404)

    def test_auth(self):
        response = self.client.get('/api/v1/feature/111111111111111111111.json') 
        self.assertEqual(json.loads(response.content),
        {u'message': u'Unauthorized - Your account credentials were invalid.', 
        u'code': u'401'})
        self.failUnlessEqual(str(response.status_code), '401') 
        

    def test_view_unknown_feature(self):     
        self.assertJsonMatchDict('/api/v1/feature/111111111111111111111.json', 
                                 {'status': 404,
                                  'total': 0,
                                  'type': "FeatureCollection",
                                  'features': []},
                                  404) 


    def test_home_page(self):     
        self.assertPageMatch('/', 'Welcome to georegistry')   
       
        
    def test_create_feature_form(self):
        url = '/api/v1/createfeature/'
        self.assertPageMatch(url, 'Upload Feature Form') 
        response = self.create_test_feature()
        self.assertEqual(str(response.status_code), "200")
        self.assertTrue("test" in response.content)        
        
  
    def test_get_feature(self):
    
        response = self.create_test_feature()
        data = json.loads(response.content)
        
        feature_id = data['features'][0]['properties']['id']
        epoch = data['features'][0]['properties']['epoch']
        
        response = self.client.get('/api/v1/feature/%s.json' % feature_id, 
                                    **self.auth) 
        self.assertTrue("test" in response.content)        
        self.assertTrue(feature_id in response.content)     
  
        response = self.client.get('/api/v1/feature/%s@%s.json' % (feature_id, 
                                                                   epoch), 
                                   **self.auth) 
        self.assertTrue("test" in response.content)
        self.assertTrue(feature_id in response.content)
        self.assertTrue(epoch in response.content)
  

    def test_search_feature(self):
    
        response = self.create_test_feature()
        data = json.loads(response.content)
        
        feature_id = data['features'][0]['properties']['id']
        epoch = data['features'][0]['properties']['epoch']
        
        response = self.client.get('/api/v1/features/search', {'feature_type': 'school'}, 
                                   **self.auth) 
        self.assertTrue("test" in response.content)        
        self.assertTrue("school" in response.content)     
  
        response = self.client.get('/api/v1/search', {'feature_type': 'church'}, 
                                       **self.auth) 
        self.assertEqual(str(response.status_code), "404")
  
  
    def test_update_feature(self):
        pass
        
        

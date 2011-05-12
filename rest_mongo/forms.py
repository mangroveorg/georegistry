#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from django import forms

from georegistry.features.utils import save_to_mongo
import json

class JsonMongoForm(forms.Form):
    """
        Form class to be used with rest_mango views that save to mongo db
        and return JSON.
    """
    
    TYPE = 'GenericCollection'

    
    def __init__(self, data=None, request=None, *args, **kwargs):
        self.request = request
        forms.Form.__init__(self, data, *args, **kwargs)
            
    
    def clean(self, *args, **kwargs):
        """
            Add the transaction uuid to the data.
        """
        if '_id' in self.cleaned_data:
            self.cleaned_data['_id'] = str(uuid.uuid4())
        if self.request:
            self.cleaned_data['owner'] = getattr(self.request.user, 'username', '')
            
            if 'urli' in self.data.keys():
                self.cleaned_data['urli'] = self.data['urli']
        new_cleaned_data={}  
        
        if not self.cleaned_data.has_key('edit'):
            for k in self.cleaned_data:
                if self.cleaned_data[k]:
                   new_cleaned_data[k]= self.cleaned_data[k]
            self.cleaned_data=new_cleaned_data
        
        return self.cleaned_data
        

    @property
    def errors(self, *args, **kwargs):
        """
            Wrap form errors in a format ready to be turned to a JSON response.
        """
        
        errors = forms.Form._get_errors(self, *args, **kwargs)
        if not errors:
            return {}
        
        return {'type':'Error',
                'status': '400',
                'results': errors}
    
    
    def save(self, tx_id=None, *args, **kwargs):
        """
            Save to data store and return the result as JSON.
        """
        
        data = save_to_mongo(self.cleaned_data, tx_id)
        return {'type': self.__class__.TYPE,
                'features': data,
                'total': len(data),
                'status': '200'}
 

from georegistry.simple_locations.gb import gbs
import json
import os
from georegistry.simple_locations.models import Area, AreaType
import slugify

def handle_uploaded_file(f, level):
    
    if level=="1":
        at=AreaType.objects.get(slug="subdivision")
        destination = open('tmp.dbf', 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        r=gbs('tmp.dbf')
        #print json.dumps(r[0], indent=4)
        os.unlink('tmp.dbf')
        for i in r:
            if i.has_key('subdivision_code') and i.has_key('country_code'):

                parent=Area.objects.get(two_letter_iso_country_code=i['country_code'],
                                        parent=None)
                Area.objects.create(name=i['NAME_1'],
                                    two_letter_iso_country_code=i['country_code'],
                                    two_letter_iso_subdivision_code=i['subdivision_code'],
                                    kind=at,
                                    parent=parent,
                                    slug=slugify.slugify(unicode(i['NAME_1']))
                                    )
        
    if level=="2":
        
        at=AreaType.objects.get(slug="level-2")
        destination = open('tmp.dbf', 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        r=gbs('tmp.dbf')
        #print json.dumps(r[0], indent=4)
        os.unlink('tmp.dbf')
        #load level 0
        for i in r:

            if i.has_key('subdivision_code') and i.has_key('country_code') \
                and i.has_key('lev2_name'):
                
                #if i['subdivision_code']=="WV":
                #    print i
                #    print ""
                
                l0=Area.objects.get(
                    two_letter_iso_country_code=i['country_code'],
                    parent=None)
                
                parent=Area.objects.get(
                    two_letter_iso_country_code=i['country_code'],
                    two_letter_iso_subdivision_code=i['subdivision_code'],
                    parent=l0)
                

                #parent=Area.objects.get(
                #    two_letter_iso_country_code=i['country_code'],
                #    two_letter_iso_subdivision_code=i['subdivision_code'],
                #    parent=l1)
            
                #print parent
                Area.objects.create(name=i['lev2_name'],
                                slug=i['lev2_slug'],
                                two_letter_iso_country_code=i['country_code'],
                                two_letter_iso_subdivision_code=i['subdivision_code'],
                                kind=at,
                                parent=parent)
                                
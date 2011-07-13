#!/usr/bin/env python


from django.conf import settings
import sys, os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import mimetypes
from datetime import datetime, timedelta
import uuid
"""
simpleS3.py
"""

#
# simpleS3.py
#
# By: Alan Viars
# Copyright Videntity Systems, Inc. 2009
# All rights Reseved.
# License: New BSD
# Last Updated: May 9, 2009
#
# This was tested using Python 2.5 and Ubuntu Linux, but
# it should run fine w/ other configurations.
# You will need to install boto to get this library running
# and of  course you need an S3 account from Amazon.
# See http://aws.amazon.com
#
# NOTES ON INSTALLING BOTO:
# 1.7.a is latestversion of boto at the time of writing.
# Execute the following from a command line prompt
# > wget http://boto.googlecode.com/files/boto-1.7a.tar.gz
# > tar zxvf boto-1.7a.tar.gz
# > cd boto-1.7a
# Run this as root or w/ admin privileges
# > python setup.py install
# > if on Ubuntu or Debian deravitive, use sudo like so:
# > sudo python setup.py install


#Set these to match your Amazon S3 Account
AWS_ACCESS_KEY= '*****PUT_YOUR_KEY_HERE****'
AWS_SECRET_ACCESS_KEY='*****PUT_YOUR_SECRET_KEY_HERE****'

class SimpleS3:
    """
    A very simple class library to simple store
    and  retieve files in Amazon S3
    Works with HTTPS/port 443 only (no HTTP/port 80)
    """

    #Store a file in s3
    def store_in_s3 (self, bucket,
                     keyname,
                     local_filepath,
                     public=False):

            """Store a file in s3"""
            url=""
            try:
                conn= S3Connection(settings.AWS_KEY,
                                   settings.AWS_SECRET)
                b = conn.create_bucket(bucket)
                k=Key(b)
                k.key=keyname

                mime = mimetypes.guess_type(keyname)[0]

                if mime==None:
                    #print "I couldn't guess MIME because"
                    #print "I couldn't detect a file ext."
                    #print "Using 'application/octet-stream'"
                    #print "as the default MIME instead."
                    mime = "application/octet-stream"

                #print "MIME Type = %s" % (mime)
                k.set_metadata("Content-Type", mime)
                print local_filepath
                k.set_contents_from_filename(local_filepath)
                if public==True:
                    k.set_acl("public-read")
                url = "https://%s.s3.amazonaws.com/%s" % (bucket,
                                                          k.key)
            except:
                print sys.exc_info()
                return url
            finally:
                return url

    #Get a file from s3
    def get_from_s3 (bucket, filename, local_filepath ):
            """Get a file from s3"""
            retval = False
            try:
                conn= S3Connection(AWS_ACCESS_KEY,
                                   AWS_SECRET_ACCESS_KEY)

                b = conn.create_bucket(bucket)
                k = Key(b)
                k.key = filename
                k.get_contents_to_filename(local_filepath)
                retval = True
            except:
                #print "Error in get_from_s3"
                #print sys.exc_info()
                return retval
            finally:
                return retval

    # Our MAIN application which takes 3 command line arguments
    # Take in a mode, bucketname, filename, and public T/F.
    # if mode=PUT, then store the file in S3
    # If mode=GET, then read the file from S3,
    # and write it to local disk

def handle_uploaded_file(file, user, uuid=str(uuid.uuid4())):
    responsedict={'localfilename':None,
                  'urli': None
                  }
    
    #create folder name for the api username
    dirname = '%s/%s/' %(settings.MEDIA_ROOT, user.username)
    
    file_name, file_ext = file.name.split(".")
    print file_name, file_ext
    try:
        #create directory if it doesn't exist
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
            
        #get a timestamp
        current_time = str(datetime.utcnow())
        time_str=current_time.replace(" ", '_')
        
        #create file name by using current datetime
        new_file_name='%s_%s.%s' %(file_name, uuid, file_ext)
        
        #create the entire directory string
        file_name='%s%s' %(dirname, new_file_name)
        full_file_path=os.path.join(settings.BASE_DIR, file_name)
        #open to write
        destination = open(file_name, 'wb')
    
        #write out in chunks
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        full_path=file_name
        file_name="%s/%s" %(user.username, new_file_name)
    except:
        responsedict['errors']="There was an error uploading your file. %s" % (str(sys.exc_info())) 
        return responsedict
    
    if settings.BINARY_STORAGE=='LOCAL':    
        responsedict['localfilename']="file://%s" % (full_path)
        responsedict['urli']=file_name    
            
    elif settings.BINARY_STORAGE=='AWSS3':
        
        s=SimpleS3()
        responsedict['urli']=s.store_in_s3 (settings.AWS_BUCKET,
                                            new_file_name,
                                            full_file_path,
                                            settings.AWS_PUBLIC)
        
        if responsedict['urli']=="":
            responsedict['errors']="AWS S3 file %s upload failed" % (new_file_name)
            
    return responsedict
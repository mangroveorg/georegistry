.. GEOREGISTRY API documentation master file, created by
   sphinx-quickstart on Wed Mar 10 10:52:08 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Georegistry API Tutorial:
=========================

.. toctree::
   :maxdepth: 3


1. Overview:
============

Georegistry is an easy to use RESTful geospatial health index designed to
improve global health through increased access to information.  It speaks
GeoJSON by default. Its hosted at georegistry.com



1.1 Technical Details:
----------------------
This document describes how to use the API (as a client), and does 
not cover Georegistry server configuration.  For server configuration, see the
RESTCat server documentation for server setup here: 

	http://github.com/mangroveorg/georegistry/README.rst
        

1.2 A Quick Example:
--------------------
The following describes how a client might fetch a geoprapic feature using the API:

	http://api.georegistry.org/api/v1/TR-7718277c-8510707da64a.json

All that needs to happen is to go to this url (and be authenticated to access
the resource).  You need a username and password to access to authenticate.

For Example, we could do this in any programming language or use a tool like curl.
::
    curl -u testuser:testpass http://api.georegistry.org/api/1.0/TR-7718277c-8510707da64a.json


The above query return a GeoJSON object which may look something like ....
::
    {
        "status": 200, 
        "total": 1, 
        "type": "FeatureCollection", 
        "features": [
            {
                "geometry": {
                    "type": "Point", 
                    "coordinates": "[0.0, 0]"
                }, 
                "type": "Feature", 
                "properties": {
                    "name": "fgf", 
                    "subdivision_code": "AH", 
                    "epoch": "1297102984", 
                    "properties_type": "school", 
                    "country_code": "GH", 
                    "_id": "7718277c-b149-4c14-9a23-8510707da64a", 
                    "id": "GR-7718277c-8510707da64a"
                }
            }
        ]
    }




 
1.3 API Methods for Manipulating Features:
---------------------------------------------------

Key:


<> = required

[] = optional



=========================================================================================== =========== ===================================================================================================================== 
BASE URL                                                                                    HTTP METHOD FUNCTION
=========================================================================================== =========== ===================================================================================================================== 
/api/1.0/createfeature/                                                                     GET/POST    POST:Create a feature in the MAIN collection. GET returns a blank form.
/api/1.0/updatefeature/<feature_id>                                                         GET/POST    POST:Update the existing feature, feature_id, in the MAIN collection. GET returns a blank form.
/api/1.0/editfeature/<feature_id>                                                           GET/POST    POST:Edit the existing feature, feature_id, in the MAIN collection. GET returns a prepopulated form.
/api/1.0/deletefeature/                                                                     GET/POST    POST:Delete the existing feature, feature_id, in the MAIN collection. GET returns a feature_id (single field) form. 
/api/1.0/collection/<collection_name>/updatefeature/<feature_id>                            GET/POST    POST:Update the existing feature, feature_id, in the collection_id. GET returns a blank form.
/api/1.0/collection/<collection_name>/editfeature/<feature_id>                              GET/POST    POST:Edit the existing feature, feature_id, in the collection_id. GET returns a prepopulated form.
/api/1.0/collection/<collection_name>/deletefeature/                                        GET/POST    POST:Delete the existing feature, feature_id, in the collection_id. GET returns a feature_id (single field) form.
=========================================================================================== =========== =====================================================================================================================




1.4 API Methods for Querying Features:
--------------------------------------

Key:


<> = required

[] = optional

=========================================================================================== =========== ==================================================================================================================== 
BASE URL                                                                                    HTTP METHOD FUNCTION
=========================================================================================== =========== ====================================================================================================================
/api/1.0/feature/<feature_id>.json                                                          GET         Get the GeoJSON Code for a feature
/api/1.0/feature/<feature_id>.png                                                           GET         Get the QR for a feature
/api/1.0/feature/<feature_id>@<epoch>.json                                                  GET         Get the GeoJSON Code for a feature at a particular epoch (timestamp)
/api/1.0/feature/<feature_id>@<epoch>.png                                                   GET         Get the QR for a feature at a particular epoch (timestamp)
/api/1.0/features/search?<some GET query string>                                            GET         Get all features that match the search dict passed in.
/api/1.0/features/country/<country_code>[-subdivision_code].json                            GET         Get all features with a particular country and or subdivision code (ISO 3166-1) eg. GH or GH-AH            
/api/1.0/features/at-point/<lat>/<lon>/                                                     GET         Get all point features at a specific lat/long point
/api/1.0/features/near-point/<lat>/<lon>/<limit>/<distance>                                 GET         Get all features near a specific lat/long point
/api/1.0/features/containing-point/<lat>/<lon>/                                             GET         Get all features containing a specific lat/long point with a limit of <limit> and a max distance of <max_distance>         
/api/1.0/features/in-boundingbox/<botleft_lon>/botleft_lat>/<topright_lon>/<topright_lat>/  GET         Get all featues in a bounding box og bottom left and top right lat/long
/api/1.0/history/feature/<feature_id>.json                                                  GET         Get the GeoJSON for a historical feature  (historical= a feature that has been suplanted by a newer version)
=========================================================================================== =========== ====================================================================================================================




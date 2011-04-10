from django.conf.urls.defaults import *
from georegistry.features.views import *
from django.views.generic.simple import direct_to_template
from georegistry.accounts.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login, logout, logout_then_login, password_change
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^simple-locations/', include('simple_locations.urls')),
   # (r'^xform_manager/', include('georegistry.xform_manager.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
        
    url(r'^accounts/register/$', 'registration.views.register', {'form_class': RegistrationForm, 'template_name': 'accounts/registration_form.html' }, name="request_account"),
    url(r'^accounts/profile/$', 'georegistry.accounts.views.account_settings', name="account_settings"),
    url(r'^login/', login, { 'template_name': 'accounts/login.html' }),
    url(r'^logout/', logout),
    url(r'^changepassword/', password_change),

    url(r'^accounts/register/complete/$', direct_to_template,
            {'template': 'registration/registration_complete.html'},
            name='registration_complete'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
            'registration.views.activate',
            {'extra_context': {'auth_form': AuthenticationForm()}},
            name='registration_activate'),
    
    #display the home page
    url(r'^$', direct_to_template, {'template': 'index.html'}),
    
    
    url(r'^api/1.0/testlogin/$', test_authorization, name="test_authorization"),
    
    #create a new feature
    url(r'^api/1.0/createfeature/$', create_feature, name="create_feature"),
    
    #update and existing feature
    url(r'^api/1.0/updatefeature/$', update_feature, name="update_feature"),
    url(r'^api/1.0/collection/(?P<collection_name>\w+)/updatefeature/$', update_feature, name="update_feature"),
    
    #update and existing feature
    url(r'^api/1.0/editfeature/(?P<feature_id>[^/]+)/$', edit_feature, name="edit_feature"), 
    url(r'^api/1.0/collection/(?P<collection_name>\w+)/editfeature/(?P<feature_id>[^/]+)/$', edit_feature, name="edit_feature"), 
    #update and existing feature
    url(r'^api/1.0/deletefeature/$', delete_feature, name="delete_feature"),
    url(r'^api/1.0/collection/(?P<collection_name>\w+)/deletefeature/$', delete_feature, name="delete_feature"),
    
    #get a feature with a particular epoch (returns a json object)
    url(r'^api/1.0/feature/(?P<feature_id>[^@]+)@(?P<epoch>[^.]+).json$', get_json_feature_by_id_and_epoch, name="get_json_feature_by_id_and_epoch"),
    
    #get a feature (returns a json object)
    url(r'^api/1.0/feature/(?P<feature_id>[^.]+).json$', get_json_feature_by_id, name="get_json_feature_by_id"),
    

    #get a QR of a feature (returns a png image)
    url(r'^api/1.0/feature/(?P<feature_id>[^@]+)@(?P<epoch>[^.]+).png$', get_qr_feature_by_id_and_epoch, name="get_qr_feature_by_id_and_epoch"),
    
    #get a QR of a feature (returns a png image)
    url(r'^api/1.0/feature/(?P<feature_id>[^.]+).png$', get_qr_feature_by_id, name="get_qr_feature_by_id"),
    
    #get the history/verified collection for a feature(returns json)
    url(r'^api/1.0/collection/(?P<collection_name>\w+)/feature/(?P<feature_id>\S+).json$', get_json_feature_by_id, name="get_json_feature_by_id"),
    
    #get all features for a country and or subdivision (returns a json list of feature_ids)
    url(r'^api/1.0/features/location/(?P<country_subdivision_code>[^.]+).json$', get_features_in_country_subdivision, name="get_features_in_country_subdivision"),
     
    #get all features that match the search dict (returns a json list of feature_ids)
    url(r'^api/1.0/features/search$', get_features_search_dict, name="get_features_search_dict"),
    
    
    #get all features at a lon/lat point
    url(r'^api/1.0/features/at-point/(?P<lat>[^/]+)/(?P<lon>[^/]+)$', get_features_at_point, name="get_features_at_point"),
    
    #get all features near a lon/lat point
    url(r'^api/1.0/features/near-point/(?P<lat>[^/]+)/(?P<lon>[^/]+)/(?P<max_distance>[^/]+)/(?P<limit>[^/]+)$', get_features_near_point, name="get_features_near_point"),
    

    #get all feautures that contain a given point(returns a json list of feature_ids)
    url(r'^api/1.0/features/containing-point/(?P<lat>\w+)/(?P<lon>\w+)$', get_features_containing_point, name="get_features_containing_point"),
    
    #get all feautures in a polygon feature(returns a json list of feature_ids)
    url(r'^api/1.0/features/geospatial/in-polygon/(?P<feature_id>\w+)$', get_features_in_polygon, name="get_features_in_polygon"),
    
    #get all feautures in a polygon feature (returns a json list of feature_ids)
    url(r'^api/1.0/features/in-boundingbox/(?P<botleft_lon>[^/]+)/(?P<botleft_lat>[^/]+)/(?P<topright_lon>[^/]+)/(?P<topright_lat>[^/]+)$', get_features_in_boundingbox, name="get_features_in_boundingbox"),

    #get a list of all feature classifiers in the system. (returns a json list of feature classifiers)
    url(r'^api/1.0/features/classifiers$', get_features_classifiers, name="get_features_classifiers"),
    
    url(r'^api/1.0/features/countries$', get_features_countries, name="get_features_countries"),
    
    url(r'^api/1.0/features/subdivisions$', get_features_subdivisions, name="get_features_subdivisions"),
    
    url(r'^api/1.0/features/locations$', get_features_locations, name="get_features_locations"),
)

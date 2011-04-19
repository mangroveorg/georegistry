from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from utils import handle_uploaded_file
from forms import UploadFileForm
from georegistry.simple_locations.models import Area, AreaType
from georegistry.simple_locations.iso3166_2letter import country_list

def import_shapefile_to_simple_locations(request, level=2):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], level)
            return HttpResponse("OK")
        else:
            return HttpResponse("NOTOK")
            
    else:
        form = UploadFileForm()
    return render_to_response('maintenance/upload.html', {'form': form},
                              context_instance = RequestContext(request),)


def load_countries_into_simple_locations(request):
    at=AreaType.objects.get(slug="country")
    for i in country_list:
        Area.objects.create(name=i['country_name'],
                            two_letter_iso_country_code=i['country_code'],
                            slug=i['country_slug'],
                            kind=at,
                            parent=None
                            )
    return HttpResponse("OK")
    
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import string, random
from .models import theURL


def home(request):
    current_site = get_current_site(request)
    return HttpResponse("<h1>Url Shortener API</h1>")

def shortIt(the_url):
    # hash configuration
    length_string = 7
    theString = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # generate random 7 length of string
    url_id = ''.join(random.choices(theString, k=length_string))
    # check if hash id is in
    # if already exists create a new
    # if not create new entry
    if not theURL.objects.filter(theHash=url_id).exists():
        created = theURL.objects.create(full_url=the_url, theHash=url_id)
        return url_id
    else:
        shortIt(the_url)

@csrf_exempt
def shorter_url(request):
    the_url = request.POST.get("url")
    # create url shorter
    hashed = shortIt(the_url)

    # get the host url
    current_site = get_current_site(request)
    data = {
        "success": True,
        "id": hashed,
        "link": "http://{}/{}".format(current_site, hashed),
        "long_url": the_url,
    }
    return JsonResponse(data)

def redirector(request, hash_id=None):
    # get value from redis key, if the value not in return Noen
    if theURL.objects.filter(theHash=hash_id).exists():
        url = theURL.objects.get(theHash=hash_id)
        # setting the value to redis for faster access
        return redirect(url.full_url)
    else:
        # if the five key not in redis and db
        return JsonResponse({"success":false})
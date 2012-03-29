from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from polls.models import Poll,Profile
import pylast
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
import md5

def profile_create(request):
    p = Profile(name=request.POST['name1'],password=request.POST['password1'],bands=request.POST['bands'])
    p.save()
    p = Profile.objects.get(name=request.POST['name1'],password=request.POST['password1'])
    request.session['profile_id'] = p.id
    request.session['password'] = p.password
    request.session['bands'] = p.bands#pull from post instead? whatevs
    return HttpResponseRedirect(reverse('polls.views.profile_return'))


def profile_login(request):
    try :
        p = Profile.objects.get(name = request.POST["name"], password = request.POST["password"])
    except:
        messages.add_message(request, messages.ERROR, 'ERROR: user not found. please try to login again')
        return HttpResponseRedirect(reverse('polls.views.login_or_create'))
    request.session['profile_id'] = p.id
    request.session['password'] = p.password
    request.session['bands'] = p.bands
    return HttpResponseRedirect(reverse('polls.views.profile_return'))




def artist(request):
    # You have to have your own unique two values for API_KEY and API_SECRET
    # Obtain yours from http://www.last.fm/api/account for Last.fm
    API_KEY = "993af2d3c49d7a02813601c0906d3376" # this is a sample key
    API_SECRET = "8dd68cb63cd4f30cf12b4148cd78676e"

    network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)

    # now you can use that object every where
    artist = network.get_artist(request.POST['artist'])

    return  HttpResponse(artist.get_bio_summary())

def artistfinder(request):
    return render_to_response('polls/artist.html',{},context_instance=RequestContext(request))

def login_or_create(request):
    return render_to_response('polls/login_or_create.html',context_instance=RequestContext(request))

def edit(request):
    p = get_object_or_404(Profile, pk = request.session['profile_id'], password = request.session['password'])
    try:
        p.bands = request.POST["bands"]
        p.save()
        messages.add_message(request, messages.INFO, 'bands changed. Thank you!' + request.POST['bands'])
        return HttpResponseRedirect(reverse('polls.views.profile_return'))
    except:
        bands = p.bands
        return render_to_response('polls/edit.html', {'bands' : bands}, context_instance = RequestContext(request))

def profile_return(request):
    profile_id = request.session['profile_id']
    password = request.session['password']
    user = get_object_or_404(Profile, pk = profile_id, password = password)
    bands = user.bands.split(',')

    API_KEY = "993af2d3c49d7a02813601c0906d3376" # this is not a sample key
    API_SECRET = "8dd68cb63cd4f30cf12b4148cd78676e"



    network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)

    bands_objects = {}
    for i in bands:
        bands_objects[i] = network.get_artist(i).get_bio_summary()
    return render_to_response('polls/profile_return.html',{'bands': bands_objects},context_instance=RequestContext(request))
















"""
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html',{'latest_poll_list' : latest_poll_list})

def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p},
                               context_instance=RequestContext(request))

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)

def info(request):
    return render_to_response('polls/info.html',{})
"""

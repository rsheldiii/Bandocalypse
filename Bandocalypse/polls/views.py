from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from polls.models import Poll,Profile
import pylast
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
import md5
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

API_KEY = "993af2d3c49d7a02813601c0906d3376" # this is a sample key
API_SECRET = "8dd68cb63cd4f30cf12b4148cd78676e"

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)



def profile_create(request):
    user = User.objects.create_user(request.POST['name'],request.POST['email'],request.POST['password'])
    user.save()
    profile = user.get_profile()
    profile.bands = request.POST['bands']
    profile.save()
    return profile_login(request)
    #return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))


def profile_login(request):
    username = request.POST['name']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:#success
            login(request, user)
            return HttpResponseRedirect(reverse('polls.views.profile_return'))
        else:
            messages.add_message(request, messages.ERROR, 'your account is inactive')
            return render_to_response('polls/login_or_create.html',context_instance=RequestContext(request))
    else:
        messages.add_message(request, messages.ERROR, 'no such account. please try again')
        return render_to_response('polls/login_or_create.html',context_instance=RequestContext(request))

@login_required
def event(request):
    try:
        request.session['bands']
        print "got the bands from the session: " + str(request.session['bands'])
    except:
        request.session['bands'] = request.user.get_profile().bands.split(',')
        print "had to generate the bands. Hopefully it worked here they are" + str(request.session['bands'])


    print "between tries"

    try:
        print "Flibbergibbet"
        place = request.POST['place']
        if place:
            print "PLACE WHAT NOW"
        geo = network.get_geo(place = place)
        events = geo.get_upcoming_events()
        
    except:
        return render_to_response('polls/event.html',context_instance=RequestContext(request))
        
    useful_events = []
    for event in events:
        b3 = []
        bands = request.session['bands']
        for artist in event.get_artists():
            artist = str(artist)
            print "your mother"
            #
            #
            #NOTE: THIS WILL PROBABLY NOT WORK IF THERE IS SOMETHING THAT IS NOT EXPRESSABLE IN ASCII INVOLVED. FIND A SOLUTION.
            #
            #
            if bands.count(artist):
                print "your father"
                b3.append(artist)
            #b3 = [str(artist) for str(artist) in event.get_artists() if str(artist) in request.session['bands']]
        print "We got out of the loop."
        if b3 != []:
            useful_events.append([event.get_artists(),event.get_title()])
        print "We got to the end of the loop succesfully."        
    print "we should execute successfully"
    return render_to_response('polls/event.html', { 'events' : useful_events },context_instance=RequestContext(request))
        
    




def artist(request):
    artist = network.get_artist(request.POST['artist'])
    return  HttpResponse(artist.get_bio_summary())

def artistfinder(request):
    return render_to_response('polls/artist.html',{},context_instance=RequestContext(request))

def home(request):
    return render_to_response('polls/login_or_create.html',context_instance=RequestContext(request))

@login_required
def edit(request):
    p = request.user.get_profile()
    try:
        p.bands = request.POST["bands"]#errors if no post data
        p.save()
        messages.add_message(request, messages.INFO, 'bands changed. Thank you!' + p.bands)
        return HttpResponseRedirect(reverse('polls.views.profile_return'))
    except:
        bands = p.bands
        return render_to_response('polls/edit.html', {'bands' : bands}, context_instance = RequestContext(request))

@login_required(login_url='/polls/accounts/login/')
def profile_return(request):
    profile = request.user.get_profile()
    bands = profile.bands.split(',')

    bands_objects = {}
    for i in bands:
        bands_objects[i] = network.get_artist(i).get_bio_summary()
    return render_to_response('polls/profile_return.html',{'bands': bands_objects},context_instance=RequestContext(request))





def info(request):
    return render_to_response('polls/info.html',{})










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


"""

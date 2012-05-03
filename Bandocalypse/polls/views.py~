from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from polls.models import Poll,Profile,Band
import pylast
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
import md5,datetime,time
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import string
import json

API_KEY = "993af2d3c49d7a02813601c0906d3376" # this is a sample key
API_SECRET = "8dd68cb63cd4f30cf12b4148cd78676e"

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)


#TODO: make single band removal function so we can add a button next to a band to remove it
#shit, we could cache so much data on our server if instead of a profile we had a database of bands associated with a database of profile numbers one to many. Then each band's shit could be cached and if it was too old when we fetched it, updated




def profile_create(request):#when we do this via ajax, the form action will be a JQuery call, sending the list in bands to a script that does this while we wait on the registration page
    print "we're in profile creator"
    try:
        user = User.objects.create_user(request.POST['name'],request.POST['email'],request.POST['password'])
        user.save()
        profile = user.get_profile()
        artists = cap_bands(request.POST['bands'])
        print artists
        print "should have fucking printed artists"
        #artists = artists.join(",")
        #artists = correct_bands(artists)
        profile.bands = artists
        profile.save()
        return profile_login(request)
    except:
        print "we excepted for some reason but python has shitty specific error handling"
        return render_to_response('polls/create.html',context_instance=RequestContext(request))
    #return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))


def profile_login(request):
    username = request.POST['name']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:#success
            login(request, user)
            return HttpResponseRedirect(reverse('polls.views.event'))
        else:
            messages.add_message(request, messages.ERROR, 'your account is inactive')
            return render_to_response('polls/login_or_create.html',context_instance=RequestContext(request))
    else:
        messages.add_message(request, messages.ERROR, 'no such account. please try again')
        return render_to_response('polls/login_or_create.html',context_instance=RequestContext(request))


def event(request,format):
    #profile
    profile = None
    try:
        if request.user.is_active:#error on user if no user
            profile = request.user.get_profile()
    except:
        print "no profile"
        
    if profile and profile.hometown:
            place = str(profile.hometown)
            print place
    #end profile
    

    
    #bands logic
    if profile:
        request.session['bands'] = profile.bands.split(',')
    else:
        request.session['bands'] = request.POST.get('bands',None)
        if request.session['bands'] is None:
            return HttpResponse("{'error':'no data'}")#exit
        
    
    if request.POST.get('place',None):
        place = str(request.POST['place'])
        print place
    
     
     
    
    #event caching block
    try:
        request.session['events'][place]
        
        if request.session['events'][place]['bands'] == request.user.get_profile().bands.split(','):
            if format == "json":
                return HttpResponse(json.dumps(request.session['events'][place]))
            return render_to_response('polls/event.html', { 'events' : request.session['events'][place]['useful events'], 'all_events' : request.session['events'][place]['all events'] },context_instance=RequestContext(request))

    except:
        print "we continue"
        
        
        
        
        
        
    #geo
    lat = request.session.get('lat',request.POST.get('lat',None))#tries session first, then POST, then sets to None
    lon = request.session.get('lon',request.POST.get('lon',None))
    
    if place:#TODO: implement geo
            print "getting geo"
            geo = network.get_geo(place = place)
            events = geo.get_upcoming_events()
            
    else:
        return render_to_response('polls/event.html',context_instance=RequestContext(request))
    

    request.session['events'] = request.session.get('events',{})



    #real logic
    request.session['events'][place] = {"all events" : [], "useful events" : []}
    all_events = request.session['events'][place]["all events"]
    useful_events = request.session['events'][place]["useful events"]
    
    for event in events:
        all_events.append([",".join([str(artist.get_name()) for artist in event.get_artists()]),str(event.get_title())])
        b3 = []
        bands = request.session['bands']
        print bands
        for artist in event.get_artists():
            artista = artist.get_name()
            print "your mother"
            #
            #
            #NOTE: THIS WILL PROBABLY NOT WORK IF THERE IS SOMETHING THAT IS NOT EXPRESSABLE IN ASCII INVOLVED. FIND A SOLUTION.
            #
            #
            if bands.count(artista):
                print "your father"
                b3.append(artist)
            
        #b3 = [str(artist) for artist in event.get_artists() if str(artist) in request.session['bands']]
        if b3 != []:
            print "we found someone"
            artists = []
            for artist in event.get_artists():
                artists.append(artist.get_name())
            
            
            useful_events.append([",".join(artists),str(event.get_title())])
            print "here are the stats for the event we are showing: " + str(event.get_title())
            
    request.session.modified = True
    request.session['events'][place]['bands'] = request.session['bands']
    
    if format == "json":
        return HttpResponse(json.dumps(request.session['events'][place]))
    return render_to_response('polls/event.html', { 'events' : useful_events, 'all_events' : all_events },context_instance=RequestContext(request))
        
    
def home(request):
    success = False
    #print "I am in home. this is my home"
    if request.user is not None:
        if request.user.is_active:#success
            success = True
            username = request.user.username
    return render_to_response('polls/login_or_create.html',{'success' : success, 'username' : username},context_instance=RequestContext(request))

@login_required
def edit(request):
    p = request.user.get_profile()
    addbands = rembands = False
    
    try:
        if request.POST["addbands"] != "":
            addbands = True
    except:
        print "no addbands"
    try:
        if request.POST["rembands"] != "":
            rembands = True
    except:
        print "no rembands"
    try:
        if request.POST["hometown"]:
            p.hometown = request.POST["hometown"]
            p.save()
    except:
        print "no hometown"
    
    
    hometown = p.hometown
    if not hometown:
        hometown = ""
    
    if rembands:
        p = request.user.get_profile()#in case both add and rem
        reverse_intersection = [artist for artist in request.session['bands'] if artist not in request.POST['rembands']]
        p.bands = cap_bands(",".join(reverse_intersection))
        p.save()
        
        
    if addbands:
        artists = cap_bands(request.POST["addbands"])#saving comma structure provided by host
        artists = ",".join([artist for artist in artists.split(",") if artist not in p.bands])#TODO: bottleneck. no way to fix. 
        
        if len(artists)>0:
            p.bands = p.bands + "," + cap_bands(artists)
            p.save()
            messages.add_message(request, messages.INFO, 'bands changed. Thank you!' + p.bands)
            request.session['bands'] = request.user.get_profile().bands.split(',')
    if not addbands and not rembands:
        bands = p.bands
        return render_to_response('polls/edit.html', {'bands' : bands.split(","), 'hometown' : hometown}, context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('polls.views.profile_return'))


@login_required(login_url='/polls/accounts/login/')
def profile_return(request):
    profile = request.user.get_profile()
    if profile.bands == "":
        #messages.add_message(request, messages.ERROR, 'you don\'t have any bands! get some bands!')#TODO: messages are queued until used. this one was building up; need to learn how to use messages better
        return render_to_response('polls/profile_return.html',context_instance=RequestContext(request))
    
    request.session['bands'] = profile.bands.split(",")

    bands_objects = get_bands(request)
    hometown = profile.hometown        
    return render_to_response('polls/profile_return.html',{'bands': bands_objects, 'hometown' : hometown},context_instance=RequestContext(request))

#band fetching helper though request.session
def get_bands(request):
    bands_objects = {}#gets fed to view; contains bands from either the network or our cache, whichever works
        #here we start caching
    for bandname in request.session['bands']:#for each named band
       
        band = Band.objects.filter(name = bandname)#filter our cache to find them!
        if not band:#if they arent in the cache
            try:
                bands_objects[bandname] = network.get_artist(i).get_bio_summary()#fetch them from the network!
            except:
                print bandname + " does not exist as a band. Saving to cache anyways"
                bands_objects[bandname] = ""
                
            b = Band(name = bandname, bio = bands_objects[bandname], last_updated = datetime.datetime.now())
            b.save()#save them to the cache
        else:
            print band#because I can
            bands_objects[bandname] = band[0].bio#because there should be only one band
            if (datetime.datetime.now() - band[0].last_updated).days > 0:#if the information is old
                bio = network.get_artist(bandname).get_bio_summary()#get new information
                band[0].bio = bio
                band[0].last_updated = datetime.datetime.now()
                band[0].save()
    return bands_objects



def info(request):
    return render_to_response('polls/info.html',{})

@login_required(login_url='/polls/accounts/login/')
def remove_all(request):
    p = request.user.get_profile()
    p.bands = ""
    p.save()
    messages.add_message(request, messages.INFO, 'all bands removed')
    return HttpResponseRedirect(reverse('polls.views.profile_return'))
    




def cap_bands(listy):#works on strings
#god damnit this doesnt work on unicode
    listy = str(listy).split(",")
    for i in range(0,len(listy)):
        listy[i] = string.capwords(listy[i])
    return ",".join(listy)








"""

def artist(request):
    artist = network.get_artist(request.POST['artist'])
    return  HttpResponse(artist.get_bio_summary())

def artistfinder(request):
    return render_to_response('polls/artist.html',{},context_instance=RequestContext(request))



def correct_bands(band_string):
    artists = []
    for item in band_string.split(","):
            try:
                artista = network.get_artist(item).get_correction()
                if artista is not None:#this was supposed to be a catch all, but it still works
                    artists.append(artista)
            except:
                print "could not instantiate artist " + item
    return artists
    
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

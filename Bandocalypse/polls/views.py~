from django.http import HttpResponse
from django.template import Context, loader
from polls.models import Poll
import pylast

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]

    return render_to_response('polls/index.html',{'latest_poll_list' : latest_poll_list})


def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html',{'poll':p})

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)

def artist_bio(request,artist):
    # You have to have your own unique two values for API_KEY and API_SECRET
    # Obtain yours from http://www.last.fm/api/account for Last.fm
    API_KEY = "993af2d3c49d7a02813601c0906d3376" # this is a sample key
    API_SECRET = "8dd68cb63cd4f30cf12b4148cd78676e"

    network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)

    # now you can use that object every where
    artist = network.get_artist(artist)

    return  HttpResponse(artist.get_bio_summary())

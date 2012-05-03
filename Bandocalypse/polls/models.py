from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.question

    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'

    def stupid(self):
	return "wootface.jpg"

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    def __unicode__(self):
        return self.choice

class Profile(models.Model):
    user = models.OneToOneField(User)
    hometown = models.CharField(max_length=200)
    bands = models.TextField()
    
class Band(models.Model):
    name = models.CharField(max_length=200)#no support for unique keys, coolio. could do database of band names and band profiles but still 
    bio = models.TextField()
    last_updated = models.DateTimeField()
    def __unicode__(self):
        return self.name + ":" + self.bio
"""
class Event(models.Model):
    name = models.CharField(max_length=200)
    bands = models.TextField()
    date = models.DateField()
    def __unicode__(self):
        return self.name + ":" + self.bio
"""

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

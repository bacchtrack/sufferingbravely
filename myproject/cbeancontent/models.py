#from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse

class LinkVoteCountManager(models.Manager):
    def get_queryset(self):
        return super(LinkVoteCountManager, self).get_queryset().annotate(votes=Count('vote')).order_by('-votes') #order by votes

class Link(models.Model):
    title = models.CharField("Headline", max_length=100)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)#the fuck this CASCADE does?
    submitted_on = models.DateTimeField(auto_now_add=True)
    rank_score = models.FloatField(default=0.0)
    url = models.URLField("URL", max_length=250, blank=True)
    description = models.TextField(blank=True)

    with_votes = LinkVoteCountManager()
    objects = models.Manager()#default manager

	#no idea what the fuck this is
    #guess it's for referencing in human-readable in queryset?
    #def __unicode__(self):
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('link_detail', kwargs={"pk": str(self.id)})

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)

    #def __unicode__(self):
    def __str__(self):
        return "%s voted %s" % (self.voter.username, self.link.title)

#class UserProfile(models.Model):
 #   user = models.OneToOneField(User, unique=True)
  #  bio = models.TextField(null=True)

   # def __str__(self): 
    #    return "%s's profile" % self.user
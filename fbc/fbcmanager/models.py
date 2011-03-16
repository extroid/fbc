from django.db import models
"""
 just look up the campaignName if url.com/BH script is called, 
 then pick a random BH url from that campaign's BH url list, 
 then append url params, then redirect
 
  each campaign has: name, BH url list, WH url
[22:27:55 MSD] rovin.v: so when a url like this is clicked: www.url.com/campaignName/?ad=1&kw=2
[22:28:34 MSD] rovin.v: it redirects to www.adobe.nu/fbc?subid=cid:campaignName+ad:1+kw+2
[22:29:10 MSD] rovin.v: which then will redirect to www.url.com/BHurl/?subid=cid:campaignName+ad:1+kw:2
[22:29:23 MSD] rovin.v: which can then decrypt the subid param and redirect to
[22:29:53 MSD] rovin.v: the campaign's random BHurl.com/?ad=1&kw=2

 
"""
from django.contrib.auth.models import User

class Campaign(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    WH_url = models.URLField(max_length=4096)
    BH_urls = models.TextField()
    
    def __unicode__ (self):
        return '%s %s BH Url [%s]' % (self.user, self.name, self.WH_url)
    
class Stats(models.Model):
    date = models.DateField(auto_now_add=True) 
    campaign = models.ForeignKey ( Campaign ) 
    incoming_clicks = models.IntegerField ( null=True, blank=True, default=0 ) 
    BH_clicks = models.IntegerField ( null=True, blank=True, default=0 ) 
    WH_clicks = models.IntegerField ( null=True, blank=True, default=0 )
    
    def campaign_name(self):
        return self.campaign.name
    campaign_name.short_description='Campaign Name'
    
    def __unicode__ (self):
        return '%s/%s %d %d %d' % (self.date, 
                                   self.campaign.name, 
                                   self.incoming_clicks, 
                                   self.BH_clicks, 
                                   self.WH_clicks)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404


from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from models import Campaign, Stats
import random

import datetime

def decode_subid(subid):
    params_map = {} 
    params = subid.split(' ')
    for param in params:
        p, v = param.split(':')
        params_map[p]=v
        
    return params_map

def encode_subid(cid, params_map):
    subid = "cid:"+cid
    for k,v in params_map.items():
        subid += '+%s:%s' % (k,v)
    return subid    

def get_stats_for_today(campaign):
    today = datetime.date.today()
    stats_q = Stats.objects.filter(date = today, campaign = campaign)
    if not stats_q.exists():
        stat_entry = Stats.objects.create(date = today, campaign = campaign)
    else:
        stat_entry = stats_q[0]
        
    return stat_entry    

def incoming(request, campaignName): 
    campaign = get_object_or_404(Campaign, name=campaignName)
    subid = encode_subid(campaign.name, request.GET)
    stats = get_stats_for_today(campaign)
    stats.incoming_clicks += 1
    stats.save()
    
    return HttpResponseRedirect('http://www.adobe.nu/fbc?subid=%s' % subid)

def process_wh_url(request):
    if request.method=='GET':
        subid = request.GET['subid']
        params = decode_subid(subid)
        campaign = get_object_or_404(Campaign, name=params['cid'])
        
        stats = get_stats_for_today(campaign)
        stats.WH_clicks += 1
        stats.save()
            
        return HttpResponseRedirect(campaign.WH_url)

def process_bh_url(request):
    if request.method=='GET':
        subid = request.GET['subid']
        params = decode_subid(subid)
        campaign = get_object_or_404(Campaign, name=params['cid'])
        
        list = campaign.BH_urls.split('\n')
        random.shuffle(list)
        
        bh_url = list[0]
        
        stats = get_stats_for_today(campaign)
        stats.BH_clicks += 1
        stats.save()
        
        return HttpResponseRedirect('%s/?subid=%s' % (bh_url, subid))
    
    
         

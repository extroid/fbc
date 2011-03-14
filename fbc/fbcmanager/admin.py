from models import Campaign, Stats
from django.contrib import admin

class CampaignAdmin(admin.ModelAdmin):
    model = Campaign
    list_display = ('user','name', )
    list_display_links = ('user','name', ) 
    
admin.site.register(Campaign, CampaignAdmin)    



class StatsAdmin(admin.ModelAdmin):
    model = Stats
    list_display = ('date','campaign_name', 'incoming_clicks', 'WH_clicks', 'BH_clicks', )
    list_display_links = ('date','campaign_name', ) 
    
admin.site.register(Stats, StatsAdmin)
"""
admin.site.register(Campaign)
admin.site.register(Stats)
"""
from django.contrib import admin
from .models import *
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone_number','checkin','time_generated']

class TravelAdmin(admin.ModelAdmin):
    list_display = ['user','travel_date','from_place','to_place','total_fare','upload_bill','time_generated']

admin.site.register(Profile,ProfileAdmin)
admin.site.register(TravelReimbursement,TravelAdmin)
admin.site.register(ProjectCategory)
admin.site.register(RegModel)
admin.site.register(Vote)
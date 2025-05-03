from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Auction)
admin.site.register(Feedback)
admin.site.register(Car)
admin.site.register(Bid)

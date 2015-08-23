from django.contrib import admin

from .forms import SubscriptionForm
from .models import Subscription

class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ["name", "__str__","show_name", "show_id", "show_date", "show_time"]
	form = SubscriptionForm
	#class Meta:
	#	model = SignUp

admin.site.register(Subscription, SubscriptionAdmin)

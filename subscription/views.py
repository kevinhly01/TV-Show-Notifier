from django.shortcuts import render
from subscription.models import Subscription

# Create your views here.
from django.http import HttpResponse
from .forms import SubscriptionForm
from tvmaze_api import Show, get_show_details
import datetime

def about(request):
	context = {
		"title": "About",
	}
	return render(request, "about.html", context)

def reminder(request):
	if request.method == 'POST':
		form = SubscriptionForm(request.POST)

		if form.is_valid():
			instance = form.save(commit = False)
			form_show = form.cleaned_data.get("show_name")
			print(form_show)
			tv_show = get_show_details(form_show)

			instance.show_id = tv_show.tv_show_id
			instance.show_name = tv_show.name
			print(tv_show.air_date)
			if tv_show.air_date != None:
				instance.show_date, instance.show_time = tv_show.air_date.split("T")
			#instance.show_date = datetime.datetime.strptime(instance.air_date, '%Y-%m-%d').date()
			
			
			#instance.timestamp = tv_show.air_date
			instance.save()
			return show_details(request, instance)
		else:
			print(form.errors)
	else:
		form = SubscriptionForm()

	title = 'Welcome'
	#subscription_list= Subscription.objects.all()
	#print(subscription_list)

	context = {
		"title": title,
		#"subscriptions": subscription_list,
		"form": form
	}
	return render(request, "home.html", context)

def show_details(request, instance):
	show_details_id= instance.show_id
	if instance.show_time:
		if ":00-04:00" in instance.show_time:
			air_date = datetime.datetime.strptime(instance.show_date, '%Y-%m-%d').strftime('%A, %B %d, %Y')
			air_time = instance.show_time.replace(":00-04:00", "")
			air_time = datetime.datetime.strptime(air_time, '%H:%M').strftime('%I:%M %p')
			show_sum= Show(show_id = show_details_id).next_ep_summary
			show_details = True
	else:
		air_date= 'TBD'
		air_time = 'TBD'
		show_sum= 'None'
		show_details = False
	
	context= {
		"Show_Details": show_details,
		"Show_Name": instance.show_name,
		"Show_Season": Show(show_id = show_details_id).curr_season,
		"Show_Network": Show(show_id = show_details_id).network,
		"Air_Date": air_date,
		"Air_Time": air_time,
		"Show_Ep": Show(show_id = show_details_id).curr_episode,
		"Show_Summary": show_sum,
		"img_url": Show(show_id = show_details_id).image
	}
	return render(request, 'show_details.html', context)
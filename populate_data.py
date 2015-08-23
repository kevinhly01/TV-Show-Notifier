import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tv_tracker.settings')

import django
django.setup()

from subscription.models import Subscription
from django.conf import settings
from django.core.mail import send_mail
from tvmaze_api import Show

import datetime

def populate():
    add_sub(name = 'Johnny',
            email = 'aassfdsds@gmail.com',
            show_name = '90210',
            show_id = '578'
            )

def add_sub(name, email, show_name, show_id):
    update_sub = Subscription.objects.filter(show_date = None)
    for name in update_sub:
        # If show no longer airs, delete request to get a notification for next episode
        if Show(show_id = name.show_id).status == 'Ended':
            name.delete()
        # Every day check if next episode air date has been release and update correspondingly
        if Show(show_id = name.show_id).air_date != None:
            name.show_date, name.show_time= Show(show_id = name.show_id).air_date.split("T")
            name.save()

    # send out subscriptions for today...
    sub = Subscription.objects.filter(show_date = datetime.date.today())
    for x in sub:
        subject = "Reminder that {} is On Today".format(x.show_name)
        from_email = settings.EMAIL_HOST_USER
        to_email = [x.email]
        # unlike name, date, time, show_sum isn't stored in database so need to go fetch it.
        episode_sum= Show(show_id= x.show_id).next_ep_summary

        contact_message = "Here is your reminder that {} airs Today, {} at {}. {}".format(x.show_name, x.show_date, x.show_time, episode_sum)
        send_mail(subject, contact_message, from_email, to_email, fail_silently= False)

        # update date table for next episode to none so duplicates aren't sent
        x.show_date = None
        x.save()

    logger.info("Saved...")

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
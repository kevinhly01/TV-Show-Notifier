from __future__ import absolute_import
from populate_data import populate
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from subscription.models import Subscription
from django.conf import settings
from django.core.mail import send_mail
from tvmaze_api import Show
import datetime

logger = get_task_logger(__name__)

@periodic_task(run_every=(crontab(hour=23, minute=45)),
    ignore_result=True)
def tasks():

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
        network = episode_sum= Show(show_id= x.show_id).network

        contact_message = "Here is a reminder that {} airs Today, {} at {} on {}. {}".format(x.show_name, x.show_date, network, x episode_sum)
        send_mail(subject, contact_message, from_email, to_email, fail_silently= False)

        # update date table for next episode to none so duplicates aren't sent
        x.show_date = None
        x.save()

	logger.info("Saved...")
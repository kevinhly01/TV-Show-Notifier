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
        to = x.email
        episode_sum= Show(show_id= x.show_id).next_ep_summary
        network= Show(show_id= x.show_id).network
        text_content = "Here is your reminder that {} airs Today, {} at {} on {}. Summary: {}".format(x.show_name, x.show_date, x.show_time, network, episode_sum)
        html_content = '<p>Here is your reminder that {} airs Today, {} at {} on {}.</p> <p> Summary: {}</p>'.format(x.show_name, x.show_date, x.show_time, network, episode_sum)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        x.show_date = None
        x.save()

	logger.info("Saved...")
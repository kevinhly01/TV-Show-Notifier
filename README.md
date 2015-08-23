# TV-Show-Notifier
TV Show Notifier is a Django Web Application that notifies subscribers when a new episode is airing. Emails are set to send daily at 
a specific time. Future plans may be to allow users to choose what time they want to be notified. However, due to constraints of hosting it on 
Heroku's free plan and the constraints, it is not viable to have a celery worker check every hour to see if a notification should be sent out.

[For a demo: http://tvshow-tracker.herokuapp.com/](http://tvshow-tracker.herokuapp.com/)

![Alt text](https://github.com/kevinhly01/TV-Show-Notifier/blob/master/TV-Show-Notifier-Features.png "Sign Up Form")

## Features:
* Form Validation that checks whether show expired + if it's invalid show
* Shows Details of next episode once user submits form.

## Purpose:
To help people remember that one of their favorite shows is airing that day

## Possible Plans For Improvement:
* Add section for users to check if their show has been cancelled and/or notification when show status (updated/cancelled) is revealed
* User-Specified time for email (Drop down list for user to select what hour of day to be notified)

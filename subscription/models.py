from django.db import models
from django.utils import timezone

# Create your models here.

class Subscription(models.Model):
	name= models.CharField(max_length = 128, blank = True, null = True)
	email = models.EmailField()
	show_name= models.CharField(max_length = 128, blank = True, null = True)
	show_id= models.CharField(max_length = 128, default = '1')
	show_date = models.DateField(blank=True, null=True)
	show_time = models.TimeField(blank=True, null=True)

	def __str__(self):
		return self.email
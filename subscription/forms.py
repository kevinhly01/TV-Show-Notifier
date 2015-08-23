from django import forms
from .models import Subscription
from tvmaze_api import Show, get_show_details
from django.core.exceptions import ValidationError

class SubscriptionForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    email = forms.EmailField()
    show_name = forms.CharField(max_length=128)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Subscription
        fields = ('name','email','show_name')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name

    def clean_show_name(self):
        show_name = self.cleaned_data.get('show_name')
        if not get_show_details(show_name):
            raise ValidationError("TV Show Not Found")
        elif get_show_details(show_name).status == 'Ended':
            raise ValidationError("TV Show Has Ended")
        return show_name

    def clean_show_id(self):
        show_id = self.cleaned_data.get('show_id')
        return show_id

    def clean_show_date(self):
        air_date = self.cleaned_data.get('air_date')
        return air_date

    def clean_show_date(self):
        air_time = self.cleaned_data.get('air_time')
        return air_time
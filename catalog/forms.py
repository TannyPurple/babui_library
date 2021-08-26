from .models import BookCopy
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class RenewBookForm(forms.Form):
    renew_date = forms.DateField(help_text= "provide a future date within next 4 weeks",)


    def clean_renew_date(self):
        data = self.cleaned_data['renew_date']
        if data < datetime.date.today():
            raise ValidationError(_('its not a future date'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('date must be within 4 weeks'))

        return data
    

class BookRenewModelForm(forms.ModelForm):
    def cleaned_due_back(self):
        data = self.cleaned_data['due_back']
        if data < datetime.date.today():
            raise ValidationError(_("You cannot extend upto a past date"))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("You cannot extend beyong 4 weeks"))
        return data 
    
    class Meta:
        model = BookCopy
        fields =  ['due_back']
        labels =  {'due_back': 'Renewal Date'}
        help_texts = {'due_back': _("Please enter a future date within next 4 weeks")}

     

 
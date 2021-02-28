import datetime
from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Book, BookInstance

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default).")

    """
    Input  validation 
        clean_<fieldname>
    """

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check if the date is in the past
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewalin past"))

        #Check if the date is within a 4 week range from the current date
        if data > datetime.date.today +datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks"))

        return data

class RenewBookModelForm(forms.ModelForm):

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        #Check if the date is in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date -renewal in past'))
        
        #Check if the date is within a 4 week range from the current date
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('invalid date - renewal more than 4 weeks ahead'))

        return data

    class Meta:
        model =BookInstance
        fields =['due_back']
        """
        Override default configuration

        """
        labels = {
            'due_back':_('New renewal date')
        }
        help_texts = {
            'due_back':_("Enter a date between now and 4 weeks")
        }


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','author','language','summary','isbn','genre']
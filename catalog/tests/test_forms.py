import datetime
from django.test import TestCase
from django.utils import timezone
from catalog.forms import RenewBookForm


# Create your tests here.


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(form.fields['renew_date'].label is None or form.fields["renew_date"].label =='renew date')

        
    def test_renew_form_date_date_field_helpself(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renew_date'].help_text,'provide a future date within next 4 weeks')


    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days =1)
        form  = RenewBookForm(data={'renew_date':date})
        self.assertFalse(form.is_valid())


    def test_renew_form_date_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days =1)
        form = RenewBookForm(data={'renew_date': date})
        self.assertFalse(form.is_valid())


    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renew_date':date})
        self.assertTrue(form.is_valid())


    def test_renew_date_max(self):
        date = timezone.localtime()+ datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renew_date':date})
        self.assertTrue(form.is_valid())
    
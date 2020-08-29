from django import forms
from django.utils import formats
from django.conf import settings
from django.core import serializers
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from django.db import transaction
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from reversion import revisions as reversion
import simplejson

from RIGS import models

# Override the django form defaults to use the HTML date/time/datetime UI elements
forms.DateField.widget = forms.DateInput(attrs={'type': 'date'})
forms.TimeField.widget = forms.TimeInput(attrs={'type': 'time'}, format='%H:%M')
forms.DateTimeField.widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d %H:%M')


# Events Shit
class EventForm(forms.ModelForm):
    datetime_input_formats = list(settings.DATETIME_INPUT_FORMATS)
    meet_at = forms.DateTimeField(input_formats=datetime_input_formats, required=False)
    access_at = forms.DateTimeField(input_formats=datetime_input_formats, required=False)

    items_json = forms.CharField()

    items = {}

    related_models = {
        'person': models.Person,
        'organisation': models.Organisation,
        'venue': models.Venue,
        'mic': models.Profile,
        'checked_in_by': models.Profile,
    }

    @property
    def _get_items_json(self):
        items = {}
        for item in self.instance.items.all():
            data = serializers.serialize('json', [item])
            struct = simplejson.loads(data)
            items[item.pk] = simplejson.dumps(struct[0])
        return simplejson.dumps(items)

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.fields['items_json'].initial = self._get_items_json
        self.fields['start_date'].widget.format = '%Y-%m-%d'
        self.fields['end_date'].widget.format = '%Y-%m-%d'

        self.fields['access_at'].widget.format = '%Y-%m-%dT%H:%M:%S'
        self.fields['meet_at'].widget.format = '%Y-%m-%dT%H:%M:%S'

    def init_items(self):
        self.items = self.process_items_json()
        return self.items

    def process_items_json(self, event=None):
        data = simplejson.loads(self.cleaned_data['items_json'])
        items = {}
        for key in data:
            pk = int(key)
            items[pk] = self._get_or_initialise_item(pk, data[key]['fields'], event)

        return items

    def _get_or_initialise_item(self, pk, data, event):
        try:
            item = models.EventItem.objects.get(pk=pk, event=event)
        except models.EventItem.DoesNotExist:
            # This occurs for one of two reasons
            # 1) The event has been duplicated, so the item PKs belong to another event
            # 2) The items are brand new, with negative PK values
            # In either case, we want to create the items
            item = models.EventItem()

        # Take the data from the form and update the item object
        item.name = data['name']
        item.description = data['description']
        item.quantity = data['quantity']
        item.cost = data['cost']
        item.order = data['order']

        if (event):
            item.event = event
            item.full_clean()
        else:
            item.full_clean('event')

        return item

    def clean(self):
        if self.cleaned_data.get("is_rig") and not (
                self.cleaned_data.get('person') or self.cleaned_data.get('organisation')):
            raise forms.ValidationError(
                'You haven\'t provided any client contact details. Please add a person or organisation.',
                code='contact')
        return super(EventForm, self).clean()

    def save(self, commit=True):
        m = super(EventForm, self).save(commit=False)

        if (commit):
            m.save()
            cur_items = m.items.all()
            items = self.process_items_json(m)
            # Delete any unneeded items
            for item in cur_items:
                if item.pk not in items:
                    item.delete()

            for key in items:
                items[key].save()

        return m

    class Meta:
        model = models.Event
        fields = ['is_rig', 'name', 'venue', 'start_time', 'end_date', 'start_date',
                  'end_time', 'meet_at', 'access_at', 'description', 'notes', 'mic',
                  'person', 'organisation', 'dry_hire', 'checked_in_by', 'status',
                  'purchase_order', 'collector']


class BaseClientEventAuthorisationForm(forms.ModelForm):
    tos = forms.BooleanField(required=True, label="Terms of hire")
    name = forms.CharField(label="Your Name")

    def clean(self):
        if self.cleaned_data.get('amount') != self.instance.event.total:
            self.add_error('amount', 'The amount authorised must equal the total for the event (inc VAT).')
        return super(BaseClientEventAuthorisationForm, self).clean()

    class Meta:
        abstract = True


class InternalClientEventAuthorisationForm(BaseClientEventAuthorisationForm):
    def __init__(self, **kwargs):
        super(InternalClientEventAuthorisationForm, self).__init__(**kwargs)
        self.fields['uni_id'].required = True
        self.fields['account_code'].required = True

    class Meta:
        model = models.EventAuthorisation
        fields = ('tos', 'name', 'amount', 'uni_id', 'account_code')


class EventAuthorisationRequestForm(forms.Form):
    email = forms.EmailField(required=True, label='Authoriser Email')


class EventRiskAssessmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventRiskAssessmentForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.__class__ == forms.BooleanField:
                field.widget = forms.RadioSelect(choices=[
                    (True, 'Yes'),
                    (False, 'No')
                ], attrs={'class': 'custom-control-input', 'required': 'true'})

    class Meta:
        model = models.RiskAssessment
        fields = '__all__'
        exclude = ['reviewed_at', 'reviewed_by']


class EventChecklistForm(forms.ModelForm):
    items = {}

    def clean(self):
        vehicles = {key: val for key, val in self.data.items()
                    if key.startswith('vehicle')}
        drivers = {key: val for key, val in self.data.items()
                   if key.startswith('driver')}
        for key in vehicles:
            pk = int(key.split('_')[1])
            driver_key = 'driver_' + str(pk)
            if(drivers[driver_key] == ''):
                raise forms.ValidationError('Add a driver to vehicle ' + str(pk), code='vehicle_mismatch')
            else:
                try:
                    item = models.EventChecklistVehicle.objects.get(pk=pk)
                except models.EventChecklistVehicle.DoesNotExist:
                    item = models.EventChecklistVehicle()

                item.vehicle = vehicles['vehicle_' + str(pk)]
                item.driver = models.Profile.objects.get(pk=drivers['driver_' + str(pk)])

                # item does not have a database pk yet as it isn't saved
                self.items[pk] = item

        return super(EventChecklistForm, self).clean()

    def save(self, commit=True):
        checklist = super(EventChecklistForm, self).save(commit=False)
        if (commit):
            # Remove all existing, to be recreated from the form
            checklist.vehicles.all().delete()
            checklist.save()

            for key in self.items:
                item = self.items[key]
                reversion.add_to_revision(item)
                # finish and save new database items
                item.checklist = checklist
                item.save()

        self.items.clear()

        return checklist

    class Meta:
        model = models.EventChecklist
        fields = '__all__'

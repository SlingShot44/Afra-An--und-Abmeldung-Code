from dataclasses import fields
from django import forms
from crispy_forms.helper import FormHelper
from API.models import Tour
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils import timezone

from API.json_tools import house_choices
from django_select2 import forms as s2forms
from crispy_forms.layout import Layout, Submit, Div

class AccountWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "first_name__icontains",
        "last_name__icontains",
    ]

class TourSearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Suchen'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = True
        self.helper.form_class = "row row-cols-auto gx-3 align-items-center w-50"
        self.helper.layout = Layout(
            Div("name", css_class="col-10"), 
            Div(
            Submit("","", css_class="search-button")
            , css_class="col-2 mb-3")
        )
    
class TourCreateForm(forms.ModelForm):
    """Form definition for Tour."""
    target = forms.ChoiceField(required=True, choices=house_choices()) 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["target"].choices = house_choices()  
    class Meta:
        """Meta definition for TourCreateform."""

        model = Tour
        fields = ('owner', 'end', 'target')
        widgets = {
            'owner': AccountWidget(attrs={'data-placeholder': 'Schüler auswählen'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
        labels = {
            'owner': 'Schüler',
            'end': 'Vermutlich zurück',
            'target': 'Ziel'
        }
    def clean_end(self):
        date = self.cleaned_data.get('end')
        if date <= timezone.now():
            raise ValidationError(_('Der gewählte Zeitpunkt liegt in der Vergangenheit'), code='invalid')
        return date

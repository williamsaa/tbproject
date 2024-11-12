# client/forms.py

from django import forms
import datetime

from .models import Client,  Address,     EmergencyContact,     EmergencyContact,  Clinical_Sypmtoms, Patient_Status, Comorbidites, MedicalFacility, Social_Assessment, Medications, Drug_susceptibility
from .models import Laboratory_Culture, Laboratory_GastricWash, Laboratory_Smear,  Laboratory_Mantoux,  Laboratory_XRay, Laboratory_PCR, Laboratory_Other
#from crispy_forms.layout import Layout, Fieldset
from crispy_forms.helper import FormHelper

from django.utils.encoding import force_str

from django_flatpickr.widgets import DatePickerInput
from crispy_forms.layout import Layout, Fieldset, Div, HTML
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from dateutil.relativedelta import *


#UserFacilityAssignmentFormSet = inlineformset_factory(User, UserFacilityAssignment, fields=('facility', 'date'), fk_name='user')


def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError("Date cannot be greater than today.")

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "date": DatePickerInput(),
        }


class Laboratory_XRayForm(forms.ModelForm):
    class Meta:
        model = Laboratory_XRay
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "xray_date": DatePickerInput(),
             "date_sample_taken": DatePickerInput(),
              "date_sample_sent": DatePickerInput(),
               "date_results_received": DatePickerInput(),
        }


class Laboratory_CultureForm(forms.ModelForm):
    class Meta:
        model = Laboratory_Culture
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "test_date": DatePickerInput(),
             "date_sample_taken": DatePickerInput(),
              "date_sample_sent": DatePickerInput(),
               "date_results_received": DatePickerInput(),
                 "date_sample_sent_to_lab": DatePickerInput(),
                 "date_sample_received_at_lab": DatePickerInput(),
        }


class Laboratory_GastricWashForm(forms.ModelForm):
    class Meta:
        model = Laboratory_GastricWash
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "test_date": DatePickerInput(),
             "date_sample_taken": DatePickerInput(),
              "date_sample_sent": DatePickerInput(),
               "date_results_received": DatePickerInput(),
        }

class Laboratory_SmearForm(forms.ModelForm):
    class Meta:
        model = Laboratory_Smear
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "test_date": DatePickerInput(),
             "date_sample_taken": DatePickerInput(),
              "date_sample_sent": DatePickerInput(),
               "date_results_received": DatePickerInput(),
                "date_sample_sent_to_lab": DatePickerInput(),
                 "date_sample_received_at_lab": DatePickerInput(),
        }


class Laboratory_MantouxForm(forms.ModelForm):
    class Meta:
        model = Laboratory_Mantoux
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "test_date": DatePickerInput(),
             "date_sample_taken": DatePickerInput(),
              "date_sample_sent": DatePickerInput(),
               "date_results_received": DatePickerInput(),
        }   

class Laboratory_PCRForm(forms.ModelForm):
    class Meta:
        model = Laboratory_PCR
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
             "date_sample_taken": DatePickerInput(),
              "date_sample_sent": DatePickerInput(),
               "date_results_received": DatePickerInput(),
                 "date_sample_sent_to_lab": DatePickerInput(),
                 "date_sample_received_at_lab": DatePickerInput(),
        }

    def clean_date_sample_taken(self):
            date = self.cleaned_data['date_sample_taken']
            if date > datetime.date.today():  # 🖘 raise error if greater than
                raise forms.ValidationError("The date_sample_taken cannot be in the future!")
            return date   
    
    def clean_date_sample_sent(self):
        date = self.cleaned_data['date_sample_sent']
        if date > datetime.date.today():  # 🖘 raise error if greater than
            raise forms.ValidationError("The date_sample_sent cannot be in the future!")
        return date   

    def clean_date_results_received(self):
        date = self.cleaned_data['date_results_received']
        if date > datetime.date.today():  # 🖘 raise error if greater than
            raise forms.ValidationError("The date_results_received cannot be in the future!")
        return date  

    def clean_date_sample_sent_to_lab(self):
        date = self.cleaned_data['date_sample_sent_to_lab']
        if date > datetime.date.today():  # 🖘 raise error if greater than
            raise forms.ValidationError("The date_sample_sent_to_lab cannot be in the future!")
        return date  
    
    def clean_date_sample_received_at_lab(self):
        date = self.cleaned_data['date_sample_received_at_lab']
        if date > datetime.date.today():  # 🖘 raise error if greater than
            raise forms.ValidationError("The date_sample_received_at_lab cannot be in the future!")
        return date  



class Laboratory_otherForm(forms.ModelForm):
    class Meta:
        model = Laboratory_Other
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
             "date_sample_taken": DatePickerInput(),
              "date_sample_sent": DatePickerInput(),
               "date_results_received": DatePickerInput(),
                 "date_sample_sent_to_lab": DatePickerInput(),
                 "date_sample_received_at_lab": DatePickerInput(),
        }

    def clean_date_sample_taken(self):
            date = self.cleaned_data['date_sample_taken']
            if date > datetime.date.today():  # 🖘 raise error if greater than
                raise forms.ValidationError("The date_sample_taken cannot be in the future!")
            return date   
    
    def clean_date_sample_sent(self):
        date = self.cleaned_data['date_sample_sent']
        if date > datetime.date.today():  # 🖘 raise error if greater than
            raise forms.ValidationError("The date_sample_sent cannot be in the future!")
        return date   

    def clean_date_results_received(self):
        date = self.cleaned_data['date_results_received']
        if date > datetime.date.today():  # 🖘 raise error if greater than
            raise forms.ValidationError("The date_results_received cannot be in the future!")
        return date  

    def clean_date_sample_sent_to_lab(self):
        date = self.cleaned_data['date_sample_sent_to_lab']
        if date > datetime.date.today():  # 🖘 raise error if greater than
            raise forms.ValidationError("The date_sample_sent_to_lab cannot be in the future!")
        return date  
    
    def clean_date_sample_received_at_lab(self):
        date = self.cleaned_data['date_sample_received_at_lab']
        if date > datetime.date.today():  # 🖘 raise error if greater than
            raise forms.ValidationError("The date_sample_received_at_lab cannot be in the future!")
        return date  




class Drug_susceptibilityForm(forms.ModelForm):
    class Meta:
        model = Drug_susceptibility
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "date": DatePickerInput(),
        }


class Social_AssessmentForm(forms.ModelForm):
    class Meta:
        model = Social_Assessment
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "date": DatePickerInput(),
        }

class MedicationsForm(forms.ModelForm):
    class Meta:
        model = Medications
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "date": DatePickerInput(),
        }



class MedicalFacilityForm(forms.ModelForm):
    class Meta:
        model = MedicalFacility
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "visit_date": DatePickerInput(),
            "discharged_date": DatePickerInput(),
            "appointment_date": DatePickerInput(),
            "admission_date": DatePickerInput(),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            "date_of_birth": DatePickerInput(),
         }
        

#class Laboratory_InvestigationForm(forms.ModelForm):
#    class Meta:
#        model = Laboratory_Investigation
#        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
#        widgets = {
#            "test_date": DatePickerInput(),
#            "date_sample_taken": DatePickerInput(),
#            "date_sample_sent": DatePickerInput(),
#            "date_results_received": DatePickerInput(),
#         }
        

class Clinical_SypmtomsForm(forms.ModelForm):
    class Meta:
        model = Clinical_Sypmtoms
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "examined_date": DatePickerInput(),
         }
               
class Patient_StatusForm(forms.ModelForm):
    class Meta:
        model = Patient_Status
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "status_date": DatePickerInput(),
             "confirmed_date": DatePickerInput(),
              "discharged_date": DatePickerInput(),
               "completed_therapy_date": DatePickerInput(),
                "treatment_outcome_date": DatePickerInput(),
                 "death_date": DatePickerInput(),
         }
                

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "date_of_birth": DatePickerInput(),
         }
        
class ComorbiditesForm(forms.ModelForm):
    class Meta:
        model = Comorbidites
        exclude = ['created_at', 'modified_on', 'created_by', 'modified_by', 'is_active', 'deleted_at', 'deleted_by', 'client', 'facility']
        widgets = {
            "examine_date": DatePickerInput(),
         }
    #date_of_birth = forms.DateField(validators=[validate_not_future_date])



        
    #date_at_address = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}))
    #date_at_address = forms.DateField(validators=[validate_not_future_date])
  

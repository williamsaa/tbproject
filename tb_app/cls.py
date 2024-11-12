# client/models.py
from datetime import datetime
import django
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .base_model import TSIS2BaseModel
from django.db.models import CheckConstraint, Q
from django.core.exceptions import ValidationError

import re


def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError("Date cannot be greater than today.")

class Client(TSIS2BaseModel):
    last_name = models.CharField(max_length=255, blank=False, null=False)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    pet_name = models.CharField(max_length=255, blank=True, null=True)
    sex_at_birth = models.ForeignKey('GenderCode', blank=False, null=False, on_delete=models.PROTECT, default=1)
    date_of_birth = models.DateField(blank=False, null=False, validators=[validate_not_future_date])
    marital_status = models.ForeignKey('MaritalStatusCode', blank=False, null=False, on_delete=models.PROTECT, default=1)
 
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    
    def save(self, *args, **kwargs):
        # Calculate the UIC based on the provided components
       
        super().save(*args, **kwargs)
# End Client model

# --------------------------------------------
class Address(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    date_at_address = models.DateField(blank=False, null=False)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    parish = models.ForeignKey("Parish", blank=False, null=False, on_delete=models.PROTECT)
    #community = models.ForeignKey('CommunityCode', blank=False, null=False,
    Community1 = models.CharField(max_length=255, blank=True, null=True)
    telephone_cell1 = models.CharField(max_length=255, blank=True, null=True)
    telephone_cell2 = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    #facility = models.ForeignKey("Facility", on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s %s" % (self.client, " - ",self.street_name, self.community1)


# --------------------------------------------
class MonthDurationCode(models.Model):
    arv_duration = models.CharField(max_length=20, blank=False, null=False)
 
    def __str__(self):
        return "%s" % (self.arv_duration)

# --------------------------------------------
class GenderCode(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=50, blank=False, null=False)
    
    def __str__(self):
        return "%s" % (self.name)
    
# --------------------------------------------
class MaritalStatusCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self):
        return "%s" % (self.name)
    
# --------------------------------------------


class Parish(TSIS2BaseModel):
    region  = models.ForeignKey("RegionCode", blank=False, null=False, on_delete=models.PROTECT)
    #1region = models.ForeignKey("Region", blank=False, null=False, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    abbreviation = models.CharField(max_length=10, blank=False, null=False, default="Unk")

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    def natural_key(self):
        return (self.name, self.code, )
    
# --------------------------------------------
class RegionManager(models.Manager):
    def get_by_natural_key(self, name, code):
        return self.get(name=name, code=code)


class RegionCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return "%s" % (self.name)

    def natural_key(self):
        return (self.name, self.code, )
 # --------------------------------------------   
class Regimen(TSIS2BaseModel):
    line = models.ForeignKey("RegimenLineCode", blank=False, null=False, related_name="regimen_line", on_delete=models.PROTECT)
    name = models.CharField(max_length=255, blank=False, null=False)
   
    def __str__(self):
        return "%s" % (self.name,)

    def natural_key(self):
        return (self.name, self.line, )
    
 # --------------------------------------------   
class RegimenLineCode(TSIS2BaseModel):
    line = models.IntegerField()
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return "%s (%s)" % (self.name, self.line)

    def natural_key(self):
        return (self.name, self.line, )
    
# --------------------------------------------



class CommunityCode(models.Model):
    code = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    parish = models.ForeignKey("Parish", blank=False, null=False, on_delete=models.PROTECT)
    deactivated_at = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s" % (self.name)
    


class ViralLoad(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    is_viral_load_request = models.BooleanField(verbose_name='Sampling for Viral Load', default=False)
    test_date = models.DateField(blank=False, null=False)
    test_result = models.FloatField(blank=True, null=True)
    undetectable = models.BooleanField(default=False)
    disa_reference_id = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    #facility = models.ForeignKey("Facility", on_delete=models.CASCADE,default=8)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

# -----------------------
class YesNoCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return "%s" % (self.name)

    def natural_key(self):
        return (self.name, self.code, )
    

# ---------------------------------

class EmergencyContact(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    date = models.DateField(blank=False, null=False)
    relationship_to_patient = models.ForeignKey('RelationshipCode', blank=False, null=False, related_name="address_occupation", on_delete=models.PROTECT)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    age_in_years = models.IntegerField(blank=True, null=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    community = models.CharField(max_length=255, blank=True, null=True)
    parish = models.ForeignKey('Parish', blank=False, null=False, related_name="emergency_contact_parish", on_delete=models.PROTECT)
    telephone_cell = models.CharField(max_length=255, blank=True, null=True)
    telephone_home = models.CharField(max_length=255, blank=True, null=True)
    telephone_work = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
   # facility = models.ForeignKey("Facility", on_delete=models.CASCADE,default=8)

    readonly_fields = ('client',)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __str__(self):
        return "%s" % (self.client)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        validation_errors = {}

        self.validate_field_community(validation_errors)
        self.validate_field_date(validation_errors)
        self.validate_field_first_name(validation_errors)
        self.validate_field_last_name(validation_errors)
        self.validate_field_parish(validation_errors)
        self.validate_field_relationship_to_patient(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)

    def validate_field_community(self, validation_errors):
        if hasattr(self, "community"):
            if self.community is None:
                validation_errors["community"] = "Community must have a value"

    def validate_field_date(self, validation_errors):
        if hasattr(self, "date"):
            if self.date is not None:
                if self.date > datetime.now().date():
                    validation_errors["date"] = "Date can not be in the future"
            else:
                validation_errors["date"] = "Date must have a value"

    def validate_field_first_name(self, validation_errors):
        if hasattr(self, "first_name"):
            if self.first_name is not None:
                if len(self.first_name) < 1 or len(self.first_name) > 50:
                    validation_errors['first_name'] = 'First name must be between 1 and 50 characters'

    def validate_field_last_name(self, validation_errors):
        if hasattr(self, "last_name"):
            if self.last_name is None:
                validation_errors['last_name'] = 'Last name must have a value'
            else:
                if len(self.last_name) < 1 or len(self.last_name) > 50:
                    validation_errors['last_name'] = 'Last name must be between 1 and 50 characters'

    def validate_field_parish(self, validation_errors):
        if hasattr(self, "parish"):
            if self.parish is None:
                validation_errors["parish"] = "Parish must have a value"

    def validate_field_relationship_to_patient(self, validation_errors):
        if hasattr(self, "relationship_to_patient"):
            if self.relationship_to_patient is None:
                validation_errors["relationship_to_patient"] = "Relationship to patient must have a value"
# --------------------------------------------

class RelationshipCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self):
        return "%s" % (self.name)
    
# --------------------------------------------

class Facility(TSIS2BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False, unique=True)
    lab_ref_code = models.CharField(max_length=255, blank=True, null=True, verbose_name='LAB reference code')
    address1 = models.CharField(max_length=255, blank=True, null=True)
    parish = models.ForeignKey("Parish", blank=False, null=False,
                               related_name='facility_parish', on_delete=models.PROTECT)
    organization = models.ForeignKey("Organization", blank=False, null=False, related_name="facility_organization", on_delete=models.PROTECT)

    def __str__(self):
        return "%s" % (self.name)

    def natural_key(self):
        return (self.name, self.code, )


# --------------------------------------------
class LabTestCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s" % (self.name)
    
# --------------------------------------------
 
class OrganizationManager(models.Manager):
    def get_by_natural_key(self, name, code):
        return self.get(name=name, code=code)

class Organization(TSIS2BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    #grant_organisation_wide_client_authorization1 = models.BooleanField(default=False)

    objects = OrganizationManager()

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        unique_together = (('name', 'code', 'deleted_at'),)
        ordering = ['name']

    def __str__(self):
        return "%s %s" % (self.code, self.name)

    def natural_key(self):
        return self.name, self.code,


#class UserFacilityAssignment(TSIS2BaseModel):

#    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.PROTECT)
    #facility = models.ForeignKey(Facility, blank=False, null=False, on_delete=models.PROTECT)
#    date = models.DateField(blank=True, null=True)

#    class Meta(object):
#        default_permissions = ('add', 'change', 'delete', 'view', 'list')
#        unique_together = (('user', 'facility'),)
#        ordering = ['user__username', 'facility__name']

    def __str__(self):
        return "%s: %s-%s" % (self.date, self.user, self.facility)
    
class PastMedicalHistory(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    performed_by = models.CharField(max_length=50, blank=True, null=True)
    report_date = models.DateField(blank=True, null=True)
    past_medical_history = models.TextField(blank=True, null=True)
    major_surgery = models.TextField(blank=True, null=True)
    allergies_medication = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        ordering = ['-report_date']
        verbose_name_plural = "Past medical histories"

    def __str__(self):
        return "%s" % (self.report_date)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)
        validation_errors = {}

        self.validate_field_report_date(validation_errors)
        self.validate_field_past_medical_historys(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)

    def validate_field_report_date(self, validation_errors):
        if hasattr(self, "report_date"):
            if self.report_date is not None:
                if self.report_date > datetime.now().date():
                    validation_errors["report_date"] = "Report date can not be in the future"
            else:
                validation_errors["report_date"] = "Report date must have a value"

    def validate_field_past_medical_historys(self, validation_errors):
        if hasattr(self, "past_medical_history"):
            if self.past_medical_history is None:
                validation_errors['past_medical_history'] = 'Past medical history cannot be left blank'
# --------------- PastMedicalHistory

class FrequencyCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)



class ContraceptiveMethodCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)
    

#------------------------
class LivingWithCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)

class HousingTypeCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)

class ToiletLocationCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)
    
class FinancialSupportCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)
    


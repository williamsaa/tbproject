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

SMEAR_RESULTS = [
    ('No AFB Seen','No AFB Seen'),
    ('1 AFB Seen / 100HPF','1 AFB Seen / 100HPF'),
    ('2 AFB Seen / 100HPF','2 AFB Seen / 100HPF'),
    ('3 AFB Seen / 100HPF','3 AFB Seen / 100HPF'),
    ('4 AFB Seen / 100HPF','4 AFB Seen / 100HPF'),
    ('5 AFB Seen / 100HPF','5 AFB Seen / 100HPF'),
    ('6 AFB Seen / 100HPF','6 AFB Seen / 100HPF'),
    ('7 AFB Seen / 100HPF','7 AFB Seen / 100HPF'),
    ('8 AFB Seen / 100HPF','8 AFB Seen / 100HPF'),
    ('9 AFB Seen / 100HPF','9 AFB Seen / 100HPF'),
    ('1+ AFB Seen','1+ AFB Seen'),
    ('2+ AFB Seen','2+ AFB Seen'),
    ('3+ AFB Seen','3+ AFB Seen'),
    ('Sample Rejected','Sample Rejected'),
    ('Test Not Done','Test Not Done'),
    ('Awaiting Result','Awaiting Result'),
]

CULTURE_RESULTS = [
    ('Growth','Growth'),
    ('No Growth','No Growth'),
    ('Contaminated','Contaminated'),
    ('Test Not Done','Test Not Done'),
    ('Awaiting Result','Awaiting Result'),
]

PCR_RESULTS = [

    ('Mycobaterium Tuberculosis Complex - Detected','Mycobaterium Tuberculosis Complex - Detected'),
    ('Mycobaterium Tuberculosis Complex - Not Detected','Mycobaterium Tuberculosis Complex - Not Detected'),
     ('Mycobaterium Tuberculosis Complex - Trace','Mycobaterium Tuberculosis Complex - Trace'),
    ('Test Not Done','Test Not Done'),
    ('Awaiting Result','Awaiting Result'),
]


SPECIMEN = [
    ('Sputum','Sputum'),
    ('Gastric Wash / Lavage','Gastric Wash / Lavage'),
    ('Bronchial Wash / Lavage','Bronchial Wash / Lavage'),
    ('Pleural Fluid','Pleural Fluid'),
    ('Urine','Urine'),
    ('Tissue','Tissue'),
    ('Cerebrospinal Fluid','Cerebrospinal Fluid'), 
    ('Ascitic Fluid','Ascitic Fluid'),   
    ('Other','Other'),
]

RESULTS = [
    ('Positive','Positive'),
    ('Negative','Negative'),
    ('Unknown','Unknown'),
    ('Test Not Done','Test Not Done')
]

MANTOUX = [
('<5 mm', '<5 mm'),
('>= 5mm (immosuppress)', '>= 5mm (immosuppress)'),
('>= 10mm (have risk factors)','>= 10mm (have risk factors)'),
('>= 15mm (no risk factors)', '>= 15mm (no risk factors)'),
('Test Not Done','Test Not Done')
]

NEW = [
    ('New','New'),
    ('Previously Treated (incomplete treatment)','Previously Treated (incomplete treatment)'),
    ('Previously Treated (Completed / New infection)','Previously Treated (Completed / New infection)'),
]


GROWTH = [
    ('Growth','Growth'),
    ('No Growth','No Growth'),
    ('Test Not Done','Test Not Done')
]


LATENT_ACTIVE = [
    ('Latent','Latent'),
    ('Active','Active')
]

PULMONARY = [
    ('Pulmonary','Pulmonary'),
    ('Extra Pulmonary','Extra Pulmonary')
]

TX_OUTCOME = [
    ('Cured','Cured'),
    ('Treatment failure','Treatment failure')

]


SEVERITY = [
    ('Mild','Mild'),
    ('Moderate','Moderate'),
    ('Severe','Severe')

]

YES_NO = [
    ('Yes','Yes'),
    ('No','No'),
    ('Dont know','Dont know'),
    ('Not stated','Not stated')
]
def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError("Date cannot be greater than today.")


PREP_MONTHS = [
    ('Last 3 months','Last 3 months'),
    ('Last 6 months','Last 6 months'),
    ('Last 12 months','Last 12 months'),
    ('Over 12 months', 'Over 12 months'),
]

class Client(TSIS2BaseModel):
    last_name = models.CharField(max_length=255, blank=False, null=False)
    #ever_taken_prep =  models.CharField(max_length=255, blank=True, null=True, choices=YES_NO)
    #prep_last_time_taken = models.CharField(max_length=255, blank=True, null=True, choices=PREP_MONTHS)

    first_name = models.CharField(max_length=255, blank=False, null=False)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    pet_name = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    sex_at_birth = models.ForeignKey('GenderCode', blank=False, null=False, on_delete=models.PROTECT)
    date_of_birth = models.DateField(blank=True, null=True, validators=[validate_not_future_date])
    age = models.IntegerField(default=0)

    #occupation = models.ForeignKey('OccupationCode', blank=False, null=False, on_delete=models.PROTECT)
    #occupation1 = models.CharField(max_length=255, blank=False, null=False)
    #marital_status = models.ForeignKey('MaritalStatusCode', blank=False, null=False, on_delete=models.PROTECT, default=1)
 
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    
    def save(self, *args, **kwargs):
        # Calculate the UIC based on the provided components     
        super().save(*args, **kwargs)
# End Client model

class OccupationCode(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=50, blank=False, null=False)
    deactivated_at = models.BooleanField(default=False)
    def __str__(self):
        return "%s" % (self.name)
# --------------------------------------------
class Address(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    date_at_address = models.DateField(blank=False, null=False)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    parish = models.ForeignKey("Parish", blank=False, null=False, on_delete=models.PROTECT)
    #community = models.ForeignKey('CommunityCode', blank=False, null=False,
    community = models.CharField(max_length=255, blank=True, null=True)
    telephone_cell1 = models.CharField(max_length=255, blank=True, null=True)
    telephone_cell2 = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    #facility = models.ForeignKey("Facility", on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s %s %s" % (self.client, " - ",self.street_name, self.community)


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
    

VISIT_TYPE = [
    ('Other','Other'),
    ('2 month','2 month'),
    ('4 month','4 month'),
    ('6 month','6 month') 
    ]

class Laboratory_Sputum(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)    
    #test_name = models.ForeignKey("LabTestCode", blank=False, null=False, on_delete=models.PROTECT, default=1)
    date_sample_taken = models.DateField(blank=False, null=False, default='2024-01-01')
    specimen_type = models.CharField(blank=False, null=False,max_length=255, choices=SPECIMEN, default=6)
    other_specimen_type =models.CharField(blank=True, null=True, max_length=255)
    date_sample_sent_to_lab = models.DateField(blank=True, null=True)
    date_sample_received_at_lab = models.DateField(blank=True, null=True)
    date_results_received = models.DateField(blank=True, null=True)
    lab_no = models.CharField(blank=True, null=True, max_length=255)
    test_results = models.CharField(blank=True, null=True, max_length=255)
    sample_rejection_reason = models.CharField(blank=True, null=True, max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')


class Laboratory_GastricWash(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)    
    date_sample_taken = models.DateField(blank=False, null=False, default='2024-01-01')
    specimen_type = models.CharField(blank=False, null=False,max_length=255, choices=SPECIMEN, default=6)
    other_specimen_type =models.CharField(blank=True, null=True, max_length=255)
    date_sample_sent_to_lab = models.DateField(blank=True, null=True)
    date_sample_received_at_lab = models.DateField(blank=True, null=True)
    date_results_received = models.DateField(blank=True, null=True)
    lab_no = models.CharField(blank=True, null=True, max_length=255)
    test_results = models.CharField(blank=True, null=True, max_length=255)
    sample_rejection_reason = models.CharField(blank=True, null=True, max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)


class Laboratory_Culture(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)    
    date_sample_taken = models.DateField(blank=False, null=False, default='2024-01-01')
    specimen_type = models.CharField(blank=False, null=False,max_length=255, choices=SPECIMEN, default=6)
    other_specimen_type =models.CharField(blank=True, null=True, max_length=255)
    date_sample_sent_to_lab = models.DateField(blank=True, null=True)
    date_sample_received_at_lab = models.DateField(blank=True, null=True)
    date_results_received = models.DateField(blank=True, null=True)
    lab_no = models.CharField(blank=True, null=True, max_length=255)
    test_results = models.CharField(blank=True, null=True, max_length=255, choices=CULTURE_RESULTS)
    organism_identified = models.CharField(blank=True, null=True, max_length=255)
    sample_rejection_reason = models.CharField(blank=True, null=True, max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)
    
class Laboratory_Mantoux(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)    
    #test_name = models.ForeignKey("LabTestCode", blank=False, null=False, on_delete=models.PROTECT, default=1)
    test_date = models.DateField(blank=False, null=False)
    #test_type_specimen = models.CharField(blank=False, null=False,max_length=255, choices=VISIT_TYPE,default=1)

    #date_sample_taken = models.DateField(blank=True, null=True)
    #date_sample_sent = models.DateField(blank=True, null=True)
    date_results_received = models.DateField(blank=True, null=True)
    test_results = models.CharField(blank=True, null=True, max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)


class Laboratory_PCR(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)    
    date_sample_taken = models.DateField(blank=False, null=False)
    specimen_type = models.CharField(blank=False, null=False,max_length=255, choices=SPECIMEN)
    other_specimen_type =models.CharField(blank=True, null=True, max_length=255)
    date_sample_sent_to_lab = models.DateField(blank=True, null=True)
    date_sample_received_at_lab = models.DateField(blank=True, null=True)
    date_results_received = models.DateField(blank=True, null=True)
    lab_no = models.CharField(blank=True, null=True, max_length=255)
    test_results = models.CharField(blank=True, null=True, max_length=255, choices=PCR_RESULTS)
    sample_rejection_reason = models.CharField(blank=True, null=True, max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)

class Laboratory_XRay(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)    
    body_part = models.ForeignKey("LabTestCode", blank=False, null=False, on_delete=models.PROTECT, default=1)
    other_body_part = models.CharField(blank=True, null=True, max_length=255)
    xray_date = models.DateField(blank=False, null=False)

    test_results = models.CharField(blank=True, null=True, max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)
    

class Laboratory_Other(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)    
    #test_name = models.ForeignKey("LabTestCode", blank=False, null=False, on_delete=models.PROTECT, default=1)
    
    date_sample_taken = models.DateField(blank=False, null=False, default='2024-01-01')
    other_specimen_type =models.CharField(blank=True, null=True, max_length=255)
    date_sample_sent_to_lab = models.DateField(blank=True, null=True)
    date_sample_received_at_lab = models.DateField(blank=True, null=True)
    date_results_received = models.DateField(blank=True, null=True)
    lab_no = models.CharField(blank=True, null=True, max_length=255)
    test_results = models.CharField(blank=True, null=True, max_length=255, choices=SMEAR_RESULTS)
    sample_rejection_reason = models.CharField(blank=True, null=True, max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)


class Laboratory_Smear(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)    
    #test_name = models.ForeignKey("LabTestCode", blank=False, null=False, on_delete=models.PROTECT, default=1)
    
    date_sample_taken = models.DateField(blank=False, null=False, default='2024-01-01')
    specimen_type = models.CharField(blank=False, null=False,max_length=255, choices=SPECIMEN, default=6)
    other_specimen_type =models.CharField(blank=True, null=True, max_length=255)
    date_sample_sent_to_lab = models.DateField(blank=True, null=True)
    date_sample_received_at_lab = models.DateField(blank=True, null=True)
    date_results_received = models.DateField(blank=True, null=True)
    lab_no = models.CharField(blank=True, null=True, max_length=255)
    test_results = models.CharField(blank=True, null=True, max_length=255, choices=SMEAR_RESULTS)
    sample_rejection_reason = models.CharField(blank=True, null=True, max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)
# -----------------------
class YesNoCode(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return "%s" % (self.name)

    def natural_key(self):
        return (self.name, self.code, )
    

class Clinical_Sypmtoms(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    assessment_date = models.DateField(blank=False, null=False)
    chronic_cough_gt_2Weeks = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    haemoptysis = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    chest_pain = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    dyspnea = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    history_of_fever = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    night_sweats = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    weight_loss	 = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    other_symptom	 = models.CharField(blank=True, null=True,max_length=255)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

# ---------------------------------

PREV_TREATED = [
    ('New','New'),
    ('Previously treated','Previously treated')
]

LATENT = [
    ('Latent','Latent'),
    ('Active','Active')
]



SEVERITY = [
    ('Mild','Mild'),
    ('Moderate','Moderate'),
     ('Severe','Severe')
]
HIV = [
    ('Positive','Positive'),
    ('Negative','Negative'),
     ('Unknown','Unknown')
]

OUTCOME = [
    ('Cured','Cured'),
    ('Therapy Failure','Therapy Failure')
]





class Patient_Status(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    status_date = models.DateField(blank=False, null=False)
    new_or_previosly_treated = models.CharField(choices=NEW,blank=True, null=True,max_length=255)
    confirmed = models.CharField(choices=YES_NO,blank=True, null=True,max_length=255)
    confirmed_date = models.DateField(blank=True, null=True,max_length=255)
    discharged = models.CharField(choices=YES_NO,blank=True, null=True,max_length=255)
    discharged_date = models.DateField(blank=True, null=True,max_length=255)
    latent_active = models.CharField(choices=LATENT_ACTIVE,blank=True, null=True,max_length=255)
    tb_location = models.CharField(choices=PULMONARY, blank=True, null=True,max_length=255)
    case_severity = models.CharField(choices=SEVERITY,blank=True, null=True,max_length=255)
    HIV_status = models.CharField(choices=HIV,blank=True, null=True,max_length=255)
    completed_therapy = models.CharField(choices=YES_NO, blank=False, null=False,max_length=255)
    completed_therapy_date = models.DateField(blank=False, null=False,max_length=255)
    incarcerated = models.CharField(choices=YES_NO,blank=True, null=True,max_length=255)
    where_incarcerated = models.CharField(blank=True, null=True,max_length=255)

    treatment_outcome = models.CharField(choices=TX_OUTCOME,blank=True, null=True,max_length=255)
    treatment_outcome_date = models.DateField(blank=True, null=True,max_length=255)

    died = models.CharField(choices=YES_NO, blank=False, null=False, max_length=255)
    death_date = models.DateField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.status_date)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')


class EmergencyContact(TSIS2BaseModel):
    client = models.ForeignKey("Client", blank=False, null=False, on_delete=models.PROTECT)
    date = models.DateField(blank=False, null=False)
    relationship_to_patient = models.ForeignKey('RelationshipCode', blank=False, null=False, related_name="address_occupation", on_delete=models.PROTECT)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    age_in_years = models.IntegerField(blank=True, null=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    community1 = models.CharField(max_length=255, blank=True, null=True)
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

        self.validate_field_community1(validation_errors)
        self.validate_field_date(validation_errors)
        self.validate_field_first_name(validation_errors)
        self.validate_field_last_name(validation_errors)
        self.validate_field_parish(validation_errors)
        self.validate_field_relationship_to_patient(validation_errors)

        if validation_errors:
            raise ValidationError(validation_errors)

    def validate_field_community1(self, validation_errors):
        if hasattr(self, "community1"):
            if self.community1 is None:
                validation_errors["community1"] = "Community must have a value"

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
    

class FrequencyCode(models.Model):
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
    
    
class Comorbidites(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    examine_date = models.DateField(blank=False, null=False)
    diabetes_mellitus	 = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    copd = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    chronic_kidney_disease	 = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    substance_abuse	 = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    malnutrition = models.CharField(blank=True, null=True,max_length=255,choices=YES_NO)
    other = models.CharField(blank=True, null=True,max_length=255)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.client, self.test_date)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'view', 'list')



class MedicalFacility(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    visit_date = models.DateField(blank=False, null=False)
    admission_date = models.DateField(blank=True, null=True)
    facility_name = models.CharField(blank=False, null=False,max_length=255)
    docket = models.CharField(blank=False, null=False,max_length=255)
    appointment_date = models.DateField(blank=True, null=True)
    missed_previous_appointment = models.CharField(blank=True, null=True,max_length=10)
    
    site_referred_from = models.CharField(blank=True, null=True,max_length=255)
    #pill_count_done = models.CharField(choices=YES_NO, blank=True, null=True, max_length=255)
    #client_adherent = models.CharField(choices=YES_NO, blank=True, null=True, max_length=255)
    discharged_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


class Drug_susceptibility(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    date = models.DateField(blank=False, null=False)
    drug_susceptibility_testing = models.CharField(choices=YES_NO, blank=True, null=True, max_length=255)
    rifampin_resistance = models.CharField(choices=YES_NO, blank=True, null=True,   max_length=255)
    multidrug_resistance = models.CharField(choices=YES_NO, blank=True, null=True,  max_length=255)
    extremely_drug_resistance = models.CharField(choices=YES_NO, blank=True, null=True,  max_length=255)
    notes = models.TextField(blank=True, null=True)

LIVING = [
    ('Lives alone','Lives alone'),
    ('Lives with partner','Lives with partner'),
    ('Lives with family','Lives with family'),

     ('Lives with friends','Lives with friends'),
    ('Homeless','Homeless'),
    ('Incarcerate','Incarcerate')
]

WORKPLACE = [
    ('Low Risk','Low Risk'),
    ('Medium Risk','Medium Risk'),
    ('High Risk','High Risk')
]


DWELLING = [
    ('Separate House-Detached','Separate House-Detached'),
    ('Apartment Building','Apartment Building'),
    ('Townhouse','Townhouse'),
     ('Part of Commercial Building','Part of Commercial Building'),
    ('Improvised Housing Unit','Improvised Housing Unit'),
    ('Non-response','Non-response'),
    ('Prison','Prison')
]


FOOD = [
    ('Consumming unpasturised milk','VConsumming unpasturised milk'),
]


class Social_Assessment(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    date = models.DateField(blank=False, null=False)
    living_arrangement = models.CharField(choices=LIVING, blank=True, null=True,   max_length=255)
    history_of_homelessness = models.CharField(choices=YES_NO, blank=True, null=True,   max_length=255)
    history_of_incarceration = models.CharField(choices=YES_NO, blank=True, null=True,   max_length=255)
    dwelling_type = models.CharField(choices=DWELLING,blank=True, null=True,   max_length=255)
    workplace_arrangement = models.CharField(choices=WORKPLACE,blank=True, null=True,   max_length=255)
    consumed_unpastuerized_milk = models.CharField(choices=YES_NO, blank=True, null=True,   max_length=255)
    
 
class tb_form_values(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    notification_date = models.DateField(blank=False, null=False)
    week_ending = models.IntegerField(blank=False, null=False)
    coordinator_name = models.CharField(blank=False, null=False,   max_length=255)



DRUG_NAME = [
    ('Isoniazid','Isoniazid'),
    ('Rifampicin','Rifampicin'),
    ('Pyrazinamide','Pyrazinamide'),
    ('Ethambutol','Ethambutol'),
    ('Streptomycin','Streptomycin'),
    ('Floxacin','Floxacin'),
    ('Other','Other'),
]


class Medications(TSIS2BaseModel):
    client = models.ForeignKey("client", blank=False, null=False, on_delete=models.PROTECT)
    date = models.DateField(blank=False, null=False)
    medication = models.CharField(choices=DRUG_NAME, blank=False, null=False, max_length=255)
    dosage = models.CharField(blank=True, null=True,   max_length=255)
    notes = models.TextField(blank=True, null=True)



from django.contrib import admin
import inspect
from .models import Client,  Address, GenderCode, MaritalStatusCode, RegionCode, RegimenLineCode, CommunityCode, Parish, Regimen, MonthDurationCode
from .models import Organization, YesNoCode, RelationshipCode, Facility, OccupationCode
from .models import LabTestCode,    EmergencyContact, Comorbidites, MedicalFacility, Drug_susceptibility, Social_Assessment, tb_form_values, Patient_Status, Clinical_Sypmtoms



from django.contrib.auth.admin import UserAdmin
admin.site.register(Comorbidites)
admin.site.register(MedicalFacility)
admin.site.register(Drug_susceptibility)
admin.site.register(Social_Assessment)
admin.site.register(tb_form_values)
admin.site.register(Patient_Status)
admin.site.register(Clinical_Sypmtoms)




admin.site.register(OccupationCode)
admin.site.register(Client)
admin.site.register(Address)
admin.site.register(GenderCode)
admin.site.register(MaritalStatusCode)
admin.site.register(RegionCode)
admin.site.register(RegimenLineCode)
admin.site.register(Regimen)
admin.site.register(CommunityCode)
admin.site.register(Parish)
admin.site.register(MonthDurationCode)
admin.site.register(YesNoCode)
admin.site.register(EmergencyContact)
admin.site.register(RelationshipCode)
admin.site.register(Facility)
admin.site.register(LabTestCode)
admin.site.register(Organization)

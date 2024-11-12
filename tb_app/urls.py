# client/urls.py

from django.urls import path
from .views import (
    close_window, fetch_communities, get_communities,
    client_list,  create_client,  edit_client,  delete_client,  client_detail,
    create_address, edit_address,  delete_address,  address_list, 

    
    clinical_symptoms_list, edit_clinical_symptoms, create_clinical_symptoms,
    patient_status_list, edit_patient_status, create_patient_status,
    comorbidities_list, edit_comorbidities, create_comorbidities,
    medical_facility_list, edit_medical_facility, create_medical_facility,
    social_assessment_list, edit_social_assessment, create_social_assessment,
    medications_list, edit_medications, create_medications,
    drug_susceptibility_list, edit_drug_susceptibility, create_drug_susceptibility,

    laboratory_culture_list, edit_laboratory_culture, delete_laboratory_culture, create_laboratory_culture,
    laboratory_xray_list, edit_laboratory_xray, delete_laboratory_xray, create_laboratory_xray,
    laboratory_mantoux_list, edit_laboratory_mantoux, create_laboratory_mantoux, delete_laboratory_mantoux,
    laboratory_pcr_list, edit_laboratory_pcr, create_laboratory_pcr, delete_laboratory_pcr,
    laboratory_gene_xpert_list, edit_laboratory_gene_xpert, create_laboratory_gene_xpert, delete_laboratory_gene_xpert,
    laboratory_gastricwash_list, edit_laboratory_gastricwash, create_laboratory_gastricwash, delete_laboratory_gastricwash,
    laboratory_smear_list, edit_laboratory_smear, create_laboratory_smear, delete_laboratory_smear,
    laboratory_other_list, edit_laboratory_other, create_laboratory_other, delete_laboratory_other,

    emergencycontact_list, edit_emergencycontact, create_emergencycontact, delete_emergencycontact,

    reports1, 

)

urlpatterns = [
    path('reports1/', reports1, name='reports1'),
    path('close_window/', close_window, name='close_window'),
    path('list/', client_list, name='client_list'),
    path('create/', create_client, name='create_client'),
    path('edit/<int:client_id>/', edit_client, name='edit_client'),
    path('delete/<int:client_id>/', delete_client, name='delete_client'),
    path('create/address/<int:client_id>/', create_address, name='create_address'),
    path('edit/address/<int:address_id>/', edit_address, name='edit_address'),
    path('delete/address/<int:address_id>/', delete_address, name='delete_address'),
   
    path('detail/<int:client_id>/', client_detail, name='client_detail'),
    #path('address_list/', address_list, name='address_list'),
    #path('client/edit/address/<int:address_id>/<int:client_id>/', edit_address, name='edit_address'),
    path('address_list/<int:client_id>/', address_list, name='address_list'),
    #path('client/address_list/<int:client_id>/', address_list, name='address_list'),
    path('create/address/<int:client_id>/', create_address, name='create_address'),
 
    path('create/emergencycontact/<int:client_id>/', create_emergencycontact, name='create_emergencycontact'),
    path('edit/emergencycontact/<int:emergencycontact_id>/', edit_emergencycontact, name='edit_emergencycontact'),
    path('delete/emergencycontact/<int:emergencycontacty_id>/', delete_emergencycontact, name='delete_emergencycontact'),
    path('emergencycontact_list/<int:client_id>/', emergencycontact_list, name='emergencycontact_list'),


    path('create/clinical_symptoms/<int:client_id>/', create_clinical_symptoms, name='create_clinical_symptoms'),
    path('edit/clinical_symptoms/<int:clinical_symptoms_id>/', edit_clinical_symptoms, name='edit_clinical_symptoms'),
    #path('delete/laboratory_investigations/<int:laboratory_investigations_id>/', dele, name='delete_emergencycontact'),
    path('clinical_symptoms_list/<int:client_id>/', clinical_symptoms_list, name='clinical_symptoms_list'),

    path('create/patient_status/<int:client_id>/', create_patient_status, name='create_patient_status'),
    path('edit/patient_status/<int:patient_status_id>/', edit_patient_status, name='edit_patient_status'),
    #path('delete/laboratory_investigations/<int:laboratory_investigations_id>/', dele, name='delete_emergencycontact'),
    path('patient_status_list/<int:client_id>/', patient_status_list, name='patient_status_list'),

   path('create/comorbidities/<int:client_id>/', create_comorbidities, name='create_comorbidities'),
    path('edit/comorbiditiess/<int:comorbidities_id>/', edit_comorbidities, name='edit_comorbidities'),
    #path('delete/laboratory_investigations/<int:laboratory_investigations_id>/', dele, name='delete_emergencycontact'),
    path('comorbidities_list/<int:client_id>/', comorbidities_list, name='comorbidities_list'),


    path('create/medical_facility/<int:client_id>/', create_medical_facility, name='create_medical_facility'),
    path('edit/medical_facility/<int:medical_facility_id>/', edit_medical_facility, name='edit_medical_facility'),
    #path('delete/laboratory_investigations/<int:laboratory_investigations_id>/', dele, name='delete_emergencycontact'),
    path('medical_facility_list/<int:client_id>/', medical_facility_list, name='medical_facility_list'),

    path('create/social_assessment/<int:client_id>/', create_social_assessment, name='create_social_assessment'),
    path('edit/social_assessment/<int:social_assessment_id>/', edit_social_assessment, name='edit_social_assessment'),
    #path('delete/laboratory_investigations/<int:laboratory_investigations_id>/', dele, name='delete_emergencycontact'),
    path('social_assessment_list/<int:client_id>/', social_assessment_list, name='social_assessment_list'),


    path('create/medications/<int:client_id>/', create_medications, name='create_medications'),
    path('edit/medications/<int:medications_id>/', edit_medications, name='edit_medications'),
    #path('delete/laboratory_investigations/<int:laboratory_investigations_id>/', dele, name='delete_emergencycontact'),
    path('medications/<int:client_id>/', medications_list, name='medications_list'),


    path('create/laboratory_culture/<int:client_id>/', create_laboratory_culture, name='create_laboratory_culture'),
    path('edit/laboratory_culture/<int:laboratory_culture_id>/', edit_laboratory_culture, name='edit_laboratory_culture'),
    path('delete/laboratory_culture/<int:laboratory_culture_id>/', delete_laboratory_culture, name='delete_laboratory_culture'),
    path('laboratory_culture_list/<int:client_id>/', laboratory_culture_list, name='laboratory_culture_list'),

    path('create/laboratory_xray/<int:client_id>/', create_laboratory_xray, name='create_laboratory_xray'),
    path('edit/laboratory_xray/<int:laboratory_xray_id>/', edit_laboratory_xray, name='edit_laboratory_xray'),
    path('delete/laboratory_xray/<int:laboratory_xray_id>/', delete_laboratory_xray, name='delete_laboratory_xray'),
    path('laboratory_xray_list/<int:client_id>/', laboratory_xray_list, name='laboratory_xray_list'),

    path('create/laboratory_mantoux/<int:client_id>/', create_laboratory_mantoux, name='create_laboratory_mantoux'),
    path('edit/laboratory_mantoux/<int:laboratory_mantoux_id>/', edit_laboratory_mantoux, name='edit_laboratory_mantoux'),
    path('delete/laboratory_mantoux/<int:laboratory_mantoux_id>/', delete_laboratory_mantoux, name='delete_laboratory_mantoux'),
    path('laboratory_mantoux_list/<int:client_id>/', laboratory_mantoux_list, name='laboratory_mantoux_list'),
    

    path('create/laboratory_pcr/<int:client_id>/', create_laboratory_pcr, name='create_laboratory_pcr'),
    path('edit/laboratory_pcr/<int:laboratory_pcr_id>/', edit_laboratory_pcr, name='edit_laboratory_pcr'),
    path('delete/laboratory_pcr/<int:laboratory_pcr_id>/', delete_laboratory_pcr, name='delete_laboratory_pcr'),
    path('laboratory_pcr_list/<int:client_id>/', laboratory_pcr_list, name='laboratory_pcr_list'),

    path('create/laboratory_gene_xpert/<int:client_id>/', create_laboratory_gene_xpert, name='create_laboratory_gene_xpert'),
    path('edit/laboratory_gene_xpert/<int:laboratory_gene_xpert_id>/', edit_laboratory_gene_xpert, name='edit_laboratory_gene_xpert'),
    path('delete/laboratory_gene_xpert/<int:laboratory_gene_xpert_id>/', delete_laboratory_gene_xpert, name='delete_laboratory_gene_xpert'),
    path('laboratory_gene_xpert_list/<int:client_id>/', laboratory_gene_xpert_list, name='laboratory_gene_xpert_list'),

    path('create/laboratory_gastricwash/<int:client_id>/', create_laboratory_gastricwash, name='create_laboratory_gastricwash'),
    path('edit/laboratory_gastricwash/<int:laboratory_gastricwash_id>/', edit_laboratory_gastricwash, name='edit_laboratory_gastricwash'),
    path('delete/laboratory_gastricwash/<int:laboratory_gastricwash_id>/', delete_laboratory_gastricwash, name='delete_laboratory_gastricwash'),
    path('laboratory_gastricwash_list/<int:client_id>/', laboratory_gastricwash_list, name='laboratory_gastricwash_list'),


    path('create/laboratory_smear/<int:client_id>/', create_laboratory_smear, name='create_laboratory_smear'),
    path('edit/laboratory_smear/<int:laboratory_smear_id>/', edit_laboratory_smear, name='edit_laboratory_smear'),
    path('delete/laboratory_smear/<int:laboratory_smear_id>/', delete_laboratory_smear, name='delete_laboratory_smear'),
    path('laboratory_smear_list/<int:client_id>/', laboratory_smear_list, name='laboratory_smear_list'),

    path('create/laboratory_other/<int:client_id>/', create_laboratory_other, name='create_laboratory_other'),
    path('edit/laboratory_other/<int:laboratory_smear_id>/', edit_laboratory_other, name='edit_laboratory_other'),
    path('delete/laboratory_other/<int:laboratory_smear_id>/', delete_laboratory_other, name='delete_laboratory_other'),
    path('laboratory_other_list/<int:client_id>/', laboratory_other_list, name='laboratory_other_list'),


    path('create/drug_susceptibility/<int:client_id>/', create_drug_susceptibility, name='create_drug_susceptibility'),
    path('edit/drug_susceptibility/<int:drug_susceptibility_id>/', edit_drug_susceptibility, name='edit_drug_susceptibility'),
    #path('delete/laboratory_investigations/<int:laboratory_investigations_id>/', dele, name='delete_emergencycontact'),
    path('drug_susceptibility_list/<int:client_id>/', drug_susceptibility_list, name='drug_susceptibility_list'),

    path('fetch_communities/', fetch_communities, name='fetch_communities'), 
    
]

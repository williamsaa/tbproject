
from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import Laboratory_CultureForm, Laboratory_GastricWashForm,  Laboratory_MantouxForm,  Laboratory_XRayForm, Laboratory_SmearForm, Laboratory_PCRForm
from .forms import ClientForm,    EmergencyContactForm, AddressForm,  Clinical_SypmtomsForm, Patient_StatusForm, ComorbiditesForm, MedicalFacilityForm, Social_AssessmentForm, MedicationsForm, Drug_susceptibilityForm
from .models import Client, Address,   EmergencyContact,    CommunityCode,  Clinical_Sypmtoms, Patient_Status, Comorbidites, MedicalFacility, Social_Assessment, Medications, Drug_susceptibility, Laboratory_Smear
from .models import Laboratory_Culture, Laboratory_GastricWash,  Laboratory_Mantoux,  Laboratory_XRay, Laboratory_PCR
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required


def close_window(request):
    return render(request, 'close_window.html')


def reports1(request):
    return render(request, 'reports1.html')


#@login_required(login_url='/accounts/login_user/')
def client_list(request):

    words = ''
    query_search = request.GET.get('query')
    
    mycs = Client.objects.filter(last_name__icontains='x87oxq123')
    mycs = Client.objects.all()

    if query_search:
        words = query_search.split()

        query = Q()
        for word in words:
            query &= Q(last_name__icontains=word) | Q(first_name__icontains=word) | Q(middle_name__icontains=word) | Q(pet_name__icontains=word)  
        
        myclients = mycs.filter(query).order_by('last_name', 'first_name').distinct()
        

    else:
        myclients = mycs.filter(last_name='zs456&^$g34@#')

    return render(request, 'client_list.html', {'clients': myclients})
#-------------------

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by_id = request.session['User_id']
            client = form.save()
            return redirect('edit_client', client_id=client.id)
    else:
        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})


def edit_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('edit_client', client_id=client_id)
    else:
        form = ClientForm(instance=client)
    return render(request, 'edit_client.html', {'form': form, 'client': client, 'client_id': client_id})


def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'delete_client.html', {'client': client})

def fetch_communities(request):
    parish_id = request.GET.get('parish_id')
    print(f"Received parish_id: {parish_id}")
    communities = CommunityCode.objects.filter(parish_id=parish_id).values('id', 'name')
    print(f"Filtered communities: {communities}")
    return JsonResponse({'communities': list(communities)})

def get_communities(request):
    parish_id = request.GET.get('parish', None)
    communities = CommunityCode.objects.filter(parish_id=parish_id).values('id', 'name')
    return JsonResponse(list(communities), safe=False)
# start address
def create_address(request, client_id):

    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            #search_value = form.cleaned_data['community_search']
            #matching_addresses = Address.objects.filter(communitycode__name__icontains=search_value)

            address = form.save(commit=False)
            address.client = client
            address.created_by_id = request.session['User_id']
            address.save()
            return render(request, 'close_window.html')

            #return redirect('edit_client', client_id=client_id)
    else:
        form = AddressForm()
    return render(request, 'create_address.html', {'form': form, 'client': client})



def edit_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    client = address.client
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.modified_by_id =  request.session['User_id']
            address.modified_on =  datetime.now()
            address.save()
            return render(request, 'close_window.html')
            #return redirect('address_list', {'address': address, 'address_id': address_id, 'client': client, 'client_id': client_id})
    else:
        form = AddressForm(instance=address)
    #return render(request, 'edit_address.html', {'form': form, 'address': address, 'address_id': address_id})
    return render(request, 'edit_address.html', {'form': form, 'address': address})


def delete_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    client = address.client
    if request.method == 'POST':
        address.delete()
        return redirect('edit_client', client_id=client.id)
    return render(request, 'delete_address.html', {'address': address, 'client': client})


def address_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    addresses = Address.objects.filter(client_id=client_id)
    return render(request, 'address_list.html', {'addresses': addresses, 'client_id': client_id})

# end adddress


def client_detail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    addresses = Address.objects.filter(client_id=client_id)

    return render(request, 'client_detail.html', {'client': client, 'addresses': addresses})

 

def create_emergencycontact(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            emergencycontact = form.save(commit=False)
            emergencycontact.client = client
            emergencycontact.created_by_id = request.session['User_id']
            emergencycontact.save()
            return render(request, 'close_window.html')

            #return redirect('edit_client', client_id=client_id)
    else:
        form = EmergencyContactForm()
    return render(request, 'create_emergencycontact.html', {'form': form, 'client': client})



def edit_emergencycontact(request, emergencycontact_id):
    emergencycontact = get_object_or_404(EmergencyContact, pk=emergencycontact_id)
    client = emergencycontact.client
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST, instance=emergencycontact)
        if form.is_valid():
            emergencycontact = form.save(commit=False)
            emergencycontact.modified_by_id =  request.session['User_id']
            emergencycontact.modified_on =  datetime.now()
            emergencycontact.save()
            return render(request, 'close_window.html')
    else:
        form = EmergencyContactForm(instance=emergencycontact)
    return render(request, 'edit_emergencycontact.html', {'form': form, 'emergencycontact': emergencycontact})


def delete_emergencycontact(request, emergencycontact_id):
    emergencycontact = get_object_or_404(EmergencyContact, pk=emergencycontact_id)
    client = emergencycontact.client
    if request.method == 'POST':
        emergencycontact.delete()
        return redirect('edit_emergencycontact', client_id=client.id)
    return render(request, 'delete_emergencycontact.html', {'emergencycontact': emergencycontact, 'client': client})


def emergencycontact_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    emergencycontact = EmergencyContact.objects.filter(client_id=client_id)
    return render(request, 'emergencycontact_list.html', {'emergencycontact': emergencycontact, 'client_id': client_id})

#clinical symptoms

def clinical_symptoms_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    clinical_symptoms = Clinical_Sypmtoms.objects.filter(client_id=client_id)
    return render(request, 'clinical_symptoms_list.html', {'clinical_symptoms': clinical_symptoms, 'client_id': client_id})

    

#-------------------

def create_clinical_symptoms(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Clinical_SypmtomsForm(request.POST)
        if form.is_valid():
            clinical_symptoms = form.save(commit=False)
            clinical_symptoms.client = client
            clinical_symptoms.created_by_id = request.session['User_id']
            clinical_symptoms.save()
            return render(request, 'close_window.html')
    else:
        form = Clinical_SypmtomsForm()
    return render(request, 'create_clinical_symptoms.html', {'form': form, 'client': client})



def edit_clinical_symptoms(request, clinical_symptoms_id):
    clinical_symptoms = get_object_or_404(Clinical_Sypmtoms, pk=clinical_symptoms_id)
    client = clinical_symptoms.client
    if request.method == 'POST':
        form = Clinical_SypmtomsForm(request.POST, instance=clinical_symptoms)
        if form.is_valid():
            clinical_symptoms = form.save(commit=False)
            clinical_symptoms.modified_by_id =  request.session['User_id']
            clinical_symptoms.modified_on =  datetime.now()
            clinical_symptoms.save()
            return render(request, 'close_window.html')
    else:
        form = Clinical_SypmtomsForm(instance=clinical_symptoms)
    return render(request, 'edit_clinical_symptoms.html', {'form': form, 'clinical_symptoms': clinical_symptoms})


#Patient Status

def patient_status_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    patient_status = Patient_Status.objects.filter(client_id=client_id)
    return render(request, 'patient_status_list.html', {'patient_status': patient_status, 'client_id': client_id})

    

#-------------------

def create_patient_status(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Patient_StatusForm(request.POST)
        if form.is_valid():
            patient_status = form.save(commit=False)
            patient_status.client = client
            patient_status.created_by_id = request.session['User_id']
            patient_status.save()
            return render(request, 'close_window.html')
    else:
        form = Patient_StatusForm()
    return render(request, 'create_patient_status.html', {'form': form, 'client': client})



def edit_patient_status(request, patient_status_id):
    patient_status = get_object_or_404(Patient_Status, pk=patient_status_id)
    client = patient_status.client
    if request.method == 'POST':
        form = Patient_StatusForm(request.POST, instance=patient_status)
        if form.is_valid():
            patient_status = form.save(commit=False)
            patient_status.modified_by_id =  request.session['User_id']
            patient_status.modified_on =  datetime.now()
            patient_status.save()
            return render(request, 'close_window.html')
    else:
        form = Patient_StatusForm(instance=patient_status)
    return render(request, 'edit_patient_status.html', {'form': form, 'patient_status': patient_status})


#COMORBIDITIES

def comorbidities_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    comorbidities = Comorbidites.objects.filter(client_id=client_id)
    return render(request, 'comorbidities_list.html', {'comorbidities': comorbidities, 'client_id': client_id})

#-------------------

def create_comorbidities(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ComorbiditesForm(request.POST)
        if form.is_valid():
            comorbidities = form.save(commit=False)
            comorbidities.client = client
            comorbidities.created_by_id = request.session['User_id']
            comorbidities.save()
            return render(request, 'close_window.html')
    else:
        form = ComorbiditesForm()
    return render(request, 'create_comorbidities.html', {'form': form, 'client': client})



def edit_comorbidities(request, comorbidities_id):
    comorbidities = get_object_or_404(Comorbidites, pk=comorbidities_id)
    client = comorbidities.client
    if request.method == 'POST':
        form = ComorbiditesForm(request.POST, instance=comorbidities)
        if form.is_valid():
            comorbidities = form.save(commit=False)
            comorbidities.modified_by_id =  request.session['User_id']
            comorbidities.modified_on =  datetime.now()
            comorbidities.save()
            return render(request, 'close_window.html')
    else:
        form = ComorbiditesForm(instance=comorbidities)
    return render(request, 'edit_comorbidities.html', {'form': form, 'comorbidities': comorbidities})



#medical_facility

def medical_facility_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    medical_facility = MedicalFacility.objects.filter(client_id=client_id)
    return render(request, 'medical_facility_list.html', {'medical_facility': medical_facility, 'client_id': client_id})

#-------------------

def create_medical_facility(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = MedicalFacilityForm(request.POST)
        if form.is_valid():
            medical_facility = form.save(commit=False)
            medical_facility.client = client
            medical_facility.created_by_id = request.session['User_id']
            medical_facility.save()
            return render(request, 'close_window.html')
    else:
        form = MedicalFacilityForm()
    return render(request, 'create_medical_facility.html', {'form': form, 'client': client})



def edit_medical_facility(request, medical_facility_id):
    medical_facility = get_object_or_404(MedicalFacility, pk=medical_facility_id)
    client = medical_facility.client
    if request.method == 'POST':
        form = MedicalFacilityForm(request.POST, instance=medical_facility)
        if form.is_valid():
            medical_facility = form.save(commit=False)
            medical_facility.modified_by_id =  request.session['User_id']
            medical_facility.modified_on =  datetime.now()
            medical_facility.save()
            return render(request, 'close_window.html')
    else:
        form = MedicalFacilityForm(instance=medical_facility)
    return render(request, 'edit_medical_facility.html', {'form': form, 'medical_facility': medical_facility})


#Social Assessment

def social_assessment_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    social_assessment = Social_Assessment.objects.filter(client_id=client_id)
    return render(request, 'social_assessment_list.html', {'social_assessment': social_assessment, 'client_id': client_id})

#-------------------

def create_social_assessment(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Social_AssessmentForm(request.POST)
        if form.is_valid():
            social_assessment = form.save(commit=False)
            social_assessment.client = client
            social_assessment.created_by_id = request.session['User_id']
            social_assessment.save()
            return render(request, 'close_window.html')
    else:
        form = Social_AssessmentForm()
    return render(request, 'create_social_assessment.html', {'form': form, 'client': client})



def edit_social_assessment(request, social_assessment_id):
    social_assessment = get_object_or_404(Social_Assessment, pk=social_assessment_id)
    client = social_assessment.client
    if request.method == 'POST':
        form = Social_AssessmentForm(request.POST, instance=social_assessment)
        if form.is_valid():
            social_assessment = form.save(commit=False)
            social_assessment.modified_by_id =  request.session['User_id']
            social_assessment.modified_on =  datetime.now()
            social_assessment.save()
            return render(request, 'close_window.html')
    else:
        form = Social_AssessmentForm(instance=social_assessment)
    return render(request, 'edit_social_assessment.html', {'form': form, 'social_assessment': social_assessment})



#Medication

def medications_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    medications = Medications.objects.filter(client_id=client_id)
    return render(request, 'medications_list.html', {'medications': medications, 'client_id': client_id})
#-------------------
def create_medications(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = MedicationsForm(request.POST)
        if form.is_valid():
            medications = form.save(commit=False)
            medications.client = client
            medications.created_by_id = request.session['User_id']
            medications.save()
            return render(request, 'close_window.html')
    else:
        form = MedicationsForm()
    return render(request, 'create_medications.html', {'form': form, 'client': client})
#-------------------

def edit_medications(request, medications_id):
    medications = get_object_or_404(Medications, pk=medications_id)
    client = medications.client
    if request.method == 'POST':
        form = MedicationsForm(request.POST, instance=medications)
        if form.is_valid():
            medications = form.save(commit=False)
            medications.modified_by_id =  request.session['User_id']
            medications.modified_on =  datetime.now()
            medications.save()
            return render(request, 'close_window.html')
    else:
        form = MedicationsForm(instance=medications)
    return render(request, 'edit_medications.html', {'form': form, 'medications': medications})



#Drug susceptibility testing

def drug_susceptibility_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    drug_susceptibility = Drug_susceptibility.objects.filter(client_id=client_id)
    return render(request, 'drug_susceptibility_list.html', {'drug_susceptibility': drug_susceptibility, 'client_id': client_id})

#-------------------

def create_drug_susceptibility(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Drug_susceptibilityForm(request.POST)
        if form.is_valid():
            drug_susceptibility = form.save(commit=False)
            drug_susceptibility.client = client
            drug_susceptibility.created_by_id = request.session['User_id']
            drug_susceptibility.save()
            return render(request, 'close_window.html')
    else:
        form = Drug_susceptibilityForm()
    return render(request, 'create_drug_susceptibility.html', {'form': form, 'client': client})



def edit_drug_susceptibility(request, drug_susceptibility_id):
    drug_susceptibility = get_object_or_404(Drug_susceptibility, pk=drug_susceptibility_id)
    client = drug_susceptibility.client
    if request.method == 'POST':
        form = Drug_susceptibilityForm(request.POST, instance=drug_susceptibility)
        if form.is_valid():
            drug_susceptibility = form.save(commit=False)
            drug_susceptibility.modified_by_id =  request.session['User_id']
            drug_susceptibility.modified_on =  datetime.now()
            drug_susceptibility.save()
            return render(request, 'close_window.html')
    else:
        form = Drug_susceptibilityForm(instance=drug_susceptibility)
    return render(request, 'edit_drug_susceptibility.html', {'form': form, 'drug_susceptibility': drug_susceptibility})

#--- Lab XRAY

def create_laboratory_xray(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Laboratory_XRayForm(request.POST)
        if form.is_valid():
            laboratory_xray = form.save(commit=False)
            laboratory_xray.client = client
            laboratory_xray.created_by_id = request.session['User_id']
            laboratory_xray.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_XRayForm()
    return render(request, 'create_laboratory_xray.html', {'form': form, 'client': client})



def edit_laboratory_xray(request, laboratory_xray_id):
    laboratory_xray = get_object_or_404(Laboratory_XRay, pk=laboratory_xray_id)
    client = laboratory_xray.client
    if request.method == 'POST':
        form = Laboratory_XRayForm(request.POST, instance=laboratory_xray)
        if form.is_valid():
            laboratory_xray = form.save(commit=False)
            laboratory_xray.modified_by_id =  request.session['User_id']
            laboratory_xray.modified_on =  datetime.now()
            laboratory_xray.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_XRayForm(instance=laboratory_xray)
    return render(request, 'edit_laboratory_xray.html', {'form': form, 'laboratory_xray': laboratory_xray})


def delete_laboratory_xray(request, laboratory_xray_id):
    laboratory_xray = get_object_or_404(Laboratory_XRay, pk=laboratory_xray_id)
    client = laboratory_xray.client
    if request.method == 'POST':
        laboratory_xray.delete()
        return redirect('edit_laboratory_xray', client_id=client.id)
    return render(request, 'delete_laboratory_xray.html', {'laboratory_xray': laboratory_xray, 'client': client})


def laboratory_xray_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    laboratory_xray = Laboratory_XRay.objects.filter(client_id=client_id)
    return render(request, 'laboratory_xray_list.html', {'laboratory_xray': laboratory_xray, 'client_id': client_id})



#--- Lab Culture

def create_laboratory_culture(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Laboratory_CultureForm(request.POST)
        if form.is_valid():
            laboratory_culture = form.save(commit=False)
            laboratory_culture.client = client
            laboratory_culture.created_by_id = request.session['User_id']
            laboratory_culture.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_CultureForm()
    return render(request, 'create_laboratory_culture.html', {'form': form, 'client': client})



def edit_laboratory_culture(request, laboratory_culture_id):
    laboratory_culture = get_object_or_404(Laboratory_Culture, pk=laboratory_culture_id)
    client = laboratory_culture.client
    if request.method == 'POST':
        form = Laboratory_CultureForm(request.POST, instance=laboratory_culture)
        if form.is_valid():
            laboratory_culture = form.save(commit=False)
            laboratory_culture.modified_by_id =  request.session['User_id']
            laboratory_culture.modified_on =  datetime.now()
            laboratory_culture.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_CultureForm(instance=laboratory_culture)
    return render(request, 'edit_laboratory_culture.html', {'form': form, 'laboratory_culture': laboratory_culture})


def delete_laboratory_culture(request, laboratory_culture_id):
    laboratory_culture = get_object_or_404(Laboratory_Culture, pk=laboratory_culture_id)
    client = laboratory_culture.client
    if request.method == 'POST':
        laboratory_culture.delete()
        return redirect('edit_laboratory_culture', client_id=client.id)
    return render(request, 'delete_laboratory_culture.html', {'laboratory_culture': laboratory_culture, 'client': client})


def laboratory_culture_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    laboratory_culture = Laboratory_Culture.objects.filter(client_id=client_id)
    return render(request, 'laboratory_culture_list.html', {'laboratory_culture': laboratory_culture, 'client_id': client_id})


#--- Lab GastricWash

def create_laboratory_gastricwash(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Laboratory_GastricWashForm(request.POST)
        if form.is_valid():
            laboratory_gastricwash = form.save(commit=False)
            laboratory_gastricwash.client = client
            laboratory_gastricwash.created_by_id = request.session['User_id']
            laboratory_gastricwash.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_GastricWashForm()
    return render(request, 'create_laboratory_gastricwash.html', {'form': form, 'client': client})

def edit_laboratory_gastricwash(request, laboratory_gastricwash_id):
    laboratory_gastricwash = get_object_or_404(Laboratory_GastricWash, pk=laboratory_gastricwash_id)
    client = laboratory_gastricwash.client
    if request.method == 'POST':
        form = Laboratory_GastricWashForm(request.POST, instance=laboratory_gastricwash)
        if form.is_valid():
            laboratory_gastricwash = form.save(commit=False)
            laboratory_gastricwash.modified_by_id =  request.session['User_id']
            laboratory_gastricwash.modified_on =  datetime.now()
            laboratory_gastricwash.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_GastricWashForm(instance=laboratory_gastricwash)
    return render(request, 'edit_laboratory_gastricwash.html', {'form': form, 'laboratory_gastricwash': laboratory_gastricwash})


def delete_laboratory_gastricwash(request, laboratory_gastricwash_id):
    laboratory_gastricwash = get_object_or_404(Laboratory_GastricWash, pk=laboratory_gastricwash_id)
    client = laboratory_gastricwash.client
    if request.method == 'POST':
        laboratory_gastricwash.delete()
        return redirect('edit_laboratory_gastricwash', client_id=client.id)
    return render(request, 'delete_laboratory_gastricwash.html', {'laboratory_gastricwash': laboratory_gastricwash, 'client': client})


def laboratory_gastricwash_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    laboratory_gastricwash = Laboratory_GastricWash.objects.filter(client_id=client_id)
    return render(request, 'laboratory_gastricwash_list.html', {'laboratory_gastricwash': laboratory_gastricwash, 'client_id': client_id})



#--- Lab Gene_Xpert

def create_laboratory_gene_xpert(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Laboratory_Gene_XpertForm(request.POST)
        if form.is_valid():
            laboratory_gene_xpert = form.save(commit=False)
            laboratory_gene_xpert.client = client
            laboratory_gene_xpert.created_by_id = request.session['User_id']
            laboratory_gene_xpert.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_Gene_XpertForm()
    return render(request, 'create_laboratory_gene_xpert.html', {'form': form, 'client': client})

def edit_laboratory_gene_xpert(request, laboratory_gene_xpert_id):
    laboratory_gene_xpert = get_object_or_404(Laboratory_Gene_Xpert, pk=laboratory_gene_xpert_id)
    client = laboratory_gene_xpert.client
    if request.method == 'POST':
        form = Laboratory_Gene_XpertForm(request.POST, instance=laboratory_gene_xpert)
        if form.is_valid():
            laboratory_gene_xpert = form.save(commit=False)
            laboratory_gene_xpert.modified_by_id =  request.session['User_id']
            laboratory_gene_xpert.modified_on =  datetime.now()
            laboratory_gene_xpert.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_Gene_XpertForm(instance=laboratory_gene_xpert)
    return render(request, 'edit_laboratory_gene_xpert.html', {'form': form, 'laboratory_gene_xpert': laboratory_gene_xpert})


def delete_laboratory_gene_xpert(request, laboratory_gene_xpert_id):
    laboratory_gene_xpert = get_object_or_404(Laboratory_Gene_Xpert, pk=laboratory_gene_xpert_id)
    client = laboratory_gene_xpert.client
    if request.method == 'POST':
        laboratory_gene_xpert.delete()
        return redirect('edit_laboratory_gene_xpert', client_id=client.id)
    return render(request, 'delete_laboratory_gene_xpert.html', {'laboratory_gene_xpert': laboratory_gene_xpert, 'client': client})


def laboratory_gene_xpert_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    laboratory_gene_xpert = Laboratory_Gene_Xpert.objects.filter(client_id=client_id)
    return render(request, 'laboratory_gene_xpert_list.html', {'laboratory_gene_xpert': laboratory_gene_xpert, 'client_id': client_id})



#--- Lab IGRA

def create_laboratory_smear(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Laboratory_SmearForm(request.POST)
        if form.is_valid():
            laboratory_smear = form.save(commit=False)
            laboratory_smear.client = client
            laboratory_smear.created_by_id = request.session['User_id']
            laboratory_smear.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_SmearForm()
    return render(request, 'create_laboratory_smear.html', {'form': form, 'client': client})

def edit_laboratory_smear(request, laboratory_smear_id):
    laboratory_smear = get_object_or_404(Laboratory_Smear, pk=laboratory_smear_id)
    client = laboratory_smear.client
    if request.method == 'POST':
        form = Laboratory_SmearForm(request.POST, instance=laboratory_smear)
        if form.is_valid():
            laboratory_smear = form.save(commit=False)
            laboratory_smear.modified_by_id =  request.session['User_id']
            laboratory_smear.modified_on =  datetime.now()
            laboratory_smear.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_SmearForm(instance=laboratory_smear)
    return render(request, 'edit_laboratory_smear.html', {'form': form, 'laboratory_smear': laboratory_smear})


def delete_laboratory_smear(request, laboratory_smear_id):
    laboratory_smear = get_object_or_404(Laboratory_Smear, pk=laboratory_smear_id)
    client = laboratory_smear.client
    if request.method == 'POST':
        laboratory_smear.delete()
        return redirect('edit_laboratory_smear', client_id=client.id)
    return render(request, 'delete_laboratory_smear.html', {'laboratory_smear': laboratory_smear, 'client': client})


def laboratory_smear_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    laboratory_smear = Laboratory_Smear.objects.filter(client_id=client_id)
    return render(request, 'laboratory_smear_list.html', {'laboratory_smear': laboratory_smear, 'client_id': client_id})



#--- Lab Mantoux

def create_laboratory_mantoux(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Laboratory_MantouxForm(request.POST)
        if form.is_valid():
            laboratory_mantoux = form.save(commit=False)
            laboratory_mantoux.client = client
            laboratory_mantoux.created_by_id = request.session['User_id']
            laboratory_mantoux.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_MantouxForm()
    return render(request, 'create_laboratory_mantoux.html', {'form': form, 'client': client})

def edit_laboratory_mantoux(request, laboratory_mantoux_id):
    laboratory_mantoux = get_object_or_404(Laboratory_Mantoux, pk=laboratory_mantoux_id)
    client = laboratory_mantoux.client
    if request.method == 'POST':
        form = Laboratory_MantouxForm(request.POST, instance=laboratory_mantoux)
        if form.is_valid():
            laboratory_mantoux = form.save(commit=False)
            laboratory_mantoux.modified_by_id =  request.session['User_id']
            laboratory_mantoux.modified_on =  datetime.now()
            laboratory_mantoux.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_MantouxForm(instance=laboratory_mantoux)
    return render(request, 'edit_laboratory_mantoux.html', {'form': form, 'laboratory_mantoux': laboratory_mantoux})


def delete_laboratory_mantoux(request, laboratory_mantoux_id):
    laboratory_mantoux = get_object_or_404(Laboratory_Mantoux, pk=laboratory_mantoux_id)
    client = laboratory_mantoux.client
    if request.method == 'POST':
        laboratory_mantoux.delete()
        return redirect('edit_laboratory_mantoux', client_id=client.id)
    return render(request, 'delete_laboratory_mantoux.html', {'laboratory_mantoux': laboratory_mantoux, 'client': client})


def laboratory_mantoux_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    laboratory_mantoux = Laboratory_Mantoux.objects.filter(client_id=client_id)
    return render(request, 'laboratory_mantoux_list.html', {'laboratory_mantoux': laboratory_mantoux, 'client_id': client_id})



#--- Lab pcr

def create_laboratory_pcr(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Laboratory_PCRForm(request.POST)
        if form.is_valid():
            laboratory_pcr = form.save(commit=False)
            laboratory_pcr.client = client
            laboratory_pcr.created_by_id = request.session['User_id']
            laboratory_pcr.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_PCRForm()
    return render(request, 'create_laboratory_pcr.html', {'form': form, 'client': client})

def edit_laboratory_pcr(request, laboratory_pcr_id):
    laboratory_pcr = get_object_or_404(Laboratory_PCR, pk=laboratory_pcr_id)
    client = laboratory_pcr.client
    if request.method == 'POST':
        form = Laboratory_PCRForm(request.POST, instance=laboratory_pcr)
        if form.is_valid():
            laboratory_pcr = form.save(commit=False)
            laboratory_pcr.modified_by_id =  request.session['User_id']
            laboratory_pcr.modified_on =  datetime.now()
            laboratory_pcr.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_PCRForm(instance=laboratory_pcr)
    return render(request, 'edit_laboratory_pcr.html', {'form': form, 'laboratory_pcr': laboratory_pcr})


def delete_laboratory_pcr(request, laboratory_pcr_id):
    laboratory_pcr = get_object_or_404(Laboratory_PCR, pk=laboratory_pcr_id)
    client = laboratory_pcr.client
    if request.method == 'POST':
        laboratory_pcr.delete()
        return redirect('edit_laboratory_pcr', client_id=client.id)
    return render(request, 'delete_laboratory_pcr.html', {'laboratory_pcr': laboratory_pcr, 'client': client})


def laboratory_pcr_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    laboratory_pcr = Laboratory_PCR.objects.filter(client_id=client_id)
    return render(request, 'laboratory_pcr_list.html', {'laboratory_pcr': laboratory_pcr, 'client_id': client_id})



#--- Lab Other


def create_laboratory_other(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = Laboratory_PCRForm(request.POST)
        if form.is_valid():
            laboratory_other = form.save(commit=False)
            laboratory_other.client = client
            laboratory_other.created_by_id = request.session['User_id']
            laboratory_other.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_PCRForm()
    return render(request, 'create_laboratory_other.html', {'form': form, 'client': client})

def edit_laboratory_other(request, laboratory_other_id):
    laboratory_other = get_object_or_404(Laboratory_PCR, pk=laboratory_other_id)
    client = laboratory_other.client
    if request.method == 'POST':
        form = Laboratory_PCRForm(request.POST, instance=laboratory_other)
        if form.is_valid():
            laboratory_other = form.save(commit=False)
            laboratory_other.modified_by_id =  request.session['User_id']
            laboratory_other.modified_on =  datetime.now()
            laboratory_other.save()
            return render(request, 'close_window.html')
    else:
        form = Laboratory_PCRForm(instance=laboratory_other)
    return render(request, 'edit_laboratory_other.html', {'form': form, 'laboratory_other': laboratory_other})


def delete_laboratory_other(request, laboratory_other_id):
    laboratory_other = get_object_or_404(Laboratory_PCR, pk=laboratory_other_id)
    client = laboratory_other.client
    if request.method == 'POST':
        laboratory_other.delete()
        return redirect('edit_laboratory_other', client_id=client.id)
    return render(request, 'delete_laboratory_other.html', {'laboratory_other': laboratory_other, 'client': client})


def laboratory_other_list(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    laboratory_other = Laboratory_PCR.objects.filter(client_id=client_id)
    return render(request, 'laboratory_other_list.html', {'laboratory_other': laboratory_other, 'client_id': client_id})


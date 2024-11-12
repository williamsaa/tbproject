from django.shortcuts import render,  redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#from tb_app.models import UserFacilityAssignment
from django.db.models import Q
from django.contrib.auth.models import User

def login_user(request):
    if request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']
        #facility1 = request.POST['facility']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            query = Q(user=user)
            #results = UserFacilityAssignment.objects.filter(query)
            request.session['User'] = username
            user1 = User.objects.get(username=user)
            user_id = user1.id
            request.session['User_id'] = user_id
            return redirect ('client_list')  
        else:
            messages.success(request,'Username or password')
            return redirect ('login_user')        
            
    return render(request, 'authentication\login.html')

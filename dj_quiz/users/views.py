from django.shortcuts import render,redirect
from .forms import RegisterForm,ParticipantRegForm
from .models import Participant
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here. for the app USers

def register(request):
    if request.method == 'POST':
        form_reg = RegisterForm(request.POST)
        form_part_reg = ParticipantRegForm(request.POST)

        if form_reg.is_valid() and form_part_reg.is_valid():
            form_reg.save(commit=True)
            form_part_reg.save(commit=True)
            phone_no = form_part_reg.cleaned_data['phone_no']
            user = User.objects.get(email=form_reg.cleaned_data['email'])

            instance = Participant.objects.get(phone_no = phone_no)
            instance.user = user
            instance.save()

            messages.success(request, f' Registeration Sucess..!\n LOGIN NOW')
            #redirect
            return redirect('login')
        else:
            print(form_reg.errors)
            print(form_part_reg.errors)
            messages.error(request,f'{form_reg.errors}')
            

            
            
               
    else:
        form_reg = RegisterForm()
        form_part_reg = ParticipantRegForm()
    

    context = {
            'form_reg':form_reg,
            'form_part_reg':form_part_reg

              }


    return render(request,'users/register.html',context)


 

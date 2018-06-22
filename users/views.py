from django.shortcuts import render 
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from . import forms

class SignIn(View):
    template_name = 'signInForm.html'
   
    def get(self, request):
        print(request.user)
        return render(request,self.template_name)
    def post(self, request):
        username = request.POST['username']        
        password = request.POST['password']
        userOne = authenticate(request, username=username, password=password)
        if userOne is not None:
            login(request, userOne)
            return HttpResponseRedirect(reverse('blockapp:index'))
        else:
            return HttpResponseRedirect(reverse('usersapp:signin'))


class SignUp(View):
    template_name = 'signupFormnew.html'
    
    def get(self, request):
        form = forms.SignUpForm()
        return render(request,self.template_name,{'form': form})
    
    def post(self, request):

        form = forms.SignUpForm(request.POST)
        if form.is_valid() :
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('blockapp:index'))
        else:
            return render(request,self.template_name,{"form": form})


class SignOut(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('usersapp:signin'))
    

# def MyIndex(request):
#     # return HttpResponse("test")
#     return render(request,'signForm.html')

# # Create your views here.

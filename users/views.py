from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

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
    template_name = 'signUpForm.html'
    
    def get(self, request):
        return render(request,self.template_name)

class SignOut(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('usersapp:signin'))
    

# def MyIndex(request):
#     # return HttpResponse("test")
#     return render(request,'signForm.html')

# # Create your views here.

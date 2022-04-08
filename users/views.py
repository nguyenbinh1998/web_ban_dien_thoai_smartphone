from django.shortcuts import redirect, render
from django.contrib import messages
from myshop.models import Customer
from .forms import UserRegisterForm

def register(request):
    if request.method == "POST":    
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save()
            Customer.objects.create(user=new_user, name=cd['username'], email=cd['email'])
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form':form})



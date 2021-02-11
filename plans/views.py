from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomSignupForm
from django.urls import reverse_lazy
from django.views import generic
from .models import FitnessPlan
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import stripe

stripe.api_key = 'sk_test_51IJQ7sFHCmVor85bcZbrjyqKKPEYU5mIYJKRKMpfcJw348grAdb9YBq2jIh4G82uXjg4gI6MOLPTXZXDv9pBnYO600Jnzva9n1'

def home(request):
    plans = FitnessPlan.objects
    return render(request, 'plans/home.html', {'plans':plans})

def plan(request,pk):
    plan = get_object_or_404(FitnessPlan, pk=pk)
    if plan.premium :
        return redirect('join')
    else:
        return render(request, 'plans/plan.html', {'plan':plan})

def join(request):
    return render(request, 'plans/join.html')

@login_required
def checkout(request):

    coupons = {'halloween':31, 'welcome':10, 'pam':60}

    if request.method == 'POST': #Carte De Credit comes thru as a post request
        return redirect('home')
    else:
        plan = 'monthly'
        coupon = 'none'
        price = 1000
        og_dollar = 10
        coupon_dollar = 0
        final_dollar = 10
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'yearly':
                plan = 'yearly'
                price = 10000
                og_dollar = 100
                final_dollar = 100

        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['coupon'].lower() in coupons:
                coupon = request.GET['coupon'].lower()
                percentage = coupons[coupon]
                coupon_price = int((percentage / 100) * price)
                price = price - coupon_price
                coupon_dollar = str(coupon_price)[:-2] + '.' + str(coupon_price)[-2:]
                final_dollar = str(price)[:-2] + '.' + str(price)[-2:]


        return render(request, 'plans/checkout.html', {'plan': plan, 'coupon': coupon, 'price': price,
        'og_dollar': og_dollar, 'final_dollar': final_dollar})

def settings(request):
    return render(request, 'registration/settings.html')

class SignUp(generic.CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid
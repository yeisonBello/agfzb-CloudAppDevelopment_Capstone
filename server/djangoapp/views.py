from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealers_from_cf, get_dealers_by_state, get_dealer_reviews_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.http import JsonResponse


logger = logging.getLogger(__name__)



def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'django/registration.html', context)

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)
    
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def about_view(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')


def get_dealerships(request):
        if request.method == "GET":
          
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/1f16b4b5-fc38-46d0-beef-cebfe392acd1/dealership-package/get-dealership"
            # Get dealers from the URL
            dealerships = get_dealers_from_cf(url)
            # Concat all dealer's short name
            dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
            # Return a list of dealer short name
            
            return HttpResponse(dealer_names)


def get_dealerships_state(request,**kwargs ):
        if request.method == "GET":
            state=kwargs.get('state')
            print(state)
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/1f16b4b5-fc38-46d0-beef-cebfe392acd1/dealership-package/get-dealership"
            # Get dealers from the URL
            dealerships = get_dealers_by_state(url,**kwargs)
            # Concat all dealer's short name
            dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
            # Return a list of dealer short name
            
            return HttpResponse(dealer_names)


def get_dealer_details(request, **kwargs):
     
     if request.method == "GET":
        dealer_id = kwargs.get('id')
        print("in the view")
        print(dealer_id)
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/1f16b4b5-fc38-46d0-beef-cebfe392acd1/dealership-package/get-review2"
        dealerships = get_dealer_reviews_from_cf(url,**kwargs)
        print(dealerships)


        # Extract short names from dealerships
        dealer_names = ' '.join([dealer.review for dealer in dealerships])
        dealer_review = [dealer.review for dealer in dealerships]
                # Return JSON response containing dealer names
        #return JsonResponse(dealerships, safe=False)
        return HttpResponse(dealer_names)

          
def add_review(request, dealer_id):
      if request.user.is_authenticated:
                 review = {
    
        "id": 1114,
        "name": "Upkar Lidder",
        "dealership": 23,
        "review": "  lovely place",
        "purchase": False,
        "another": "field",
        "purchase_date": "02/16/2020",
        "car_make": "Audi",
        "car_model": "Car",
        "car_year": 2021
    
}

                 json_payload = {}
                 json_payload["review"] = review # thi is r=the request body
                 url="https://us-south.functions.appdomain.cloud/api/v1/web/1f16b4b5-fc38-46d0-beef-cebfe392acd1/dealership-package/post_review"
                 post_request(url, json_payload, dealerId=dealer_id)
                 return redirect("djangoapp:dealer_details", id=dealer_id)

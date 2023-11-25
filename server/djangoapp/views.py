from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf,post_request, get_dealer_by_id_from_cf# get_dealers_by_state,
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
        context = {}
        if request.method == "GET":
            
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/1f16b4b5-fc38-46d0-beef-cebfe392acd1/dealership-package/get-dealership"
            # Get dealers from the URL
            dealerships = get_dealers_from_cf(url)
            context["dealership_list"] = dealerships
            # Concat all dealer's short name
            #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
            # Return a list of dealer short name
            
            return render(request, 'djangoapp/index.html', context)


# def get_dealerships_state(request,**kwargs ):
#         if request.method == "GET":
#             state=kwargs.get('state')
#             print(state)
#             url = "https://us-south.functions.appdomain.cloud/api/v1/web/1f16b4b5-fc38-46d0-beef-cebfe392acd1/dealership-package/get-dealership"
#             # Get dealers from the URL
#             dealerships = get_dealers_by_state(url,**kwargs)
#             # Concat all dealer's short name
#             dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
#             # Return a list of dealer short name
            
#             return HttpResponse(dealer_names)



def get_dealer_details(request, **kwargs):
    if request.method == "GET":
        context = {}
        dealer_id = kwargs.get('id')
        name = request.GET.get('name')
        context["name"] = name
        context["id"] = dealer_id
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/1f16b4b5-fc38-46d0-beef-cebfe392acd1/dealership-package/get-review2"
        reviews = get_dealer_reviews_from_cf(url, **kwargs)
        context["reviews_list"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)



def add_review(request, dealer_id):
  
    if request.user.is_authenticated:
      
        if request.method == "GET":
            context = {}
            name = request.GET.get('name')
            context["name"] = name
            cars = list(CarModel.objects.filter(dealer_id=dealer_id))
            print(cars)
            for car in cars:
                car.year = car.year.strftime("%Y")
               
            context["cars"] = cars
            context["dealer_id"] = dealer_id

            return render(request, "djangoapp/add_review.html", context)

        if request.method == "POST":
            user = request.user
            review = {}
            review["id"] = dealer_id
            review["time"] = datetime.utcnow().isoformat()
            # extract the information from user
            review["name"] = f"{user.first_name} {user.last_name}"
            print( review["name"])
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']
            checked = request.POST.get('purchasecheck', False)

            if checked == "on":
                checked = True
            review["purchase"] = checked
            review["purchase_date"] = request.POST['purchasedate']
            car_model, car_make, car_year = request.POST['car_details'].split("-")
            review["car_make"] = car_make
            review["car_model"] = car_model
            review["car_year"] = car_year
            url="https://us-south.functions.appdomain.cloud/api/v1/web/1f16b4b5-fc38-46d0-beef-cebfe392acd1/dealership-package/post_review"
            json_payload = {}
            json_payload["review"] = review
            post_request(url, json_payload, dealerId=dealer_id)
            print("Review submitted.")

            return redirect("djangoapp:dealer_details", id=dealer_id)
            
    else: 
        print("User is not authenticated")
        return redirect("djangoapp:dealer_details", id=dealer_id)


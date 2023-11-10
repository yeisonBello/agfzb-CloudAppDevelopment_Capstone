import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, SentimentOptions

import datetime

def get_request(url, **kwargs):
   
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "api_key" in kwargs:
            # Basic authentication GET
            params = dict()
            params["language"] = "en"
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            print(params)
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params, auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealers_by_state(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# def get_dealer_reviews_from_cf(url, **kwargs):
   
#     results = []
#     # Ensure 'dealerId' key is present in kwargs
#     dealer_id = kwargs.get('id')
#     print(dealer_id)

#     if dealer_id is None:
#         # Handle the case where 'dealerId' is not provided
#         print("Error: 'dealer_id' is missing in kwargs")
#         return results
#     json_result = get_request(url, **kwargs)
#     if json_result:
#         # Get the list of reviews from JSON response
#         reviews = json_result
#         print(reviews)
        
#         # For each review object
#         for review in reviews:
        
#          review_doc = review
#          print(review_doc)
#             # Create a DealerReview object with values from the review object
#         review_obj = DealerReview(
#                 dealership=kwargs.get('id'),
#                 # name=review_doc["name"],
#                 purchase=review_doc["purchase"],
#                 review=review_doc["review"],
#                 purchase_date=review_doc["purchase_date"],
#                 car_make=review_doc["car_make"],
#                 car_model=review_doc["car_model"],
#                 car_year=review_doc["car_year"],
#                 sentiment=review_doc["sentiment"],
#                 id=review_doc["id"]
#             )
#         results.append(review_obj)

#     return results


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    dealer_id = kwargs.get('id')
    
    if dealer_id is None:
        print("Error: 'dealer_id' is missing in kwargs")
        return results
    
    json_result = get_request(url, **kwargs)
    
    if json_result:
        reviews = json_result.get('data', {}).get('docs', [])
        
        for doc in reviews:
            review_obj = DealerReview(
                dealership=dealer_id,
                name=doc.get("name"),
                purchase=doc.get("purchase"),
                review=doc.get("review"),
                purchase_date=doc.get("purchase_date"),
                car_make=doc.get("car_make"),
                car_model=doc.get("car_model"),
                car_year=doc.get("car_year"),
                id=doc.get("id"),
                sentiment="i hate this place the people is really rude",
            )
            # Assuming analyze_review_sentiments() returns the sentiment analysis result
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    
    return results


# def get_dealer_reviews_from_cf(url, **kwargs):
   
#     results = []
#     dealer_id = kwargs.get('id')
#     if dealer_id is None:
#         # Handle the case where 'dealerId' is not provided
#         print("Error: 'dealer_id' is missing in kwargs")
#         return results
#     json_result = get_request(url, **kwargs)
#     if json_result:
#         reviews = json_result
#         docs = reviews['data']['docs']
#         cont=0
#         for doc in docs:
#          cont=cont+1 
   
#             # Create a DealerReview object with values from the review object
#          review_obj = DealerReview(
#                 dealership=kwargs.get('id'),
#                 name=doc["name"],
#                 purchase=doc["purchase"],
#                 review=doc["review"],
#                 purchase_date=doc["purchase_date"],
#                 car_make=doc["car_make"],
#                 car_model=doc["car_model"],
#                 car_year=doc["car_year"],
#                 sentiment="i hate this place the people is really rude",
#                 id=doc["id"])
#                review_obj.sentiment = analyze_review_sentiments(review_obj.review)
#     results.append(review_obj)
#     print(cont)
#     return results

# def get_dealer_reviews_from_cf(url, **kwargs):
#     results = []
#     dealer_id = kwargs.get('id')
#     json_result = get_request(url, dealerId=dealer_id)
#     if json_result:
#         reviews = json_result
#         print(reviews)
#         for review in reviews:
#             review_doc = review
           
           
#             print("in the loop")
#             print(review_doc[0])
#             print("in the loop2")
#             review_obj = DealerReview( dealership=kwargs.get('id'),  purchase=34, 
#                                     review=review_doc["review"], car_make=review_doc["car_make"], car_model=review_doc["car_model"],
#                                     car_year=review_doc["car_year"], id=review_doc["id"], purchase_date=review_doc["purchase_date"],
#                                     sentiment="sentiment")
#             review_obj.sentiment = analyze_review_sentiments(review_obj.review)
#             # if review_obj.purchase_date:
#             #     review_obj.purchase_date = datetime.datetime.strptime(review_obj.purchase_date, '%m/%d/%Y')            
#             results.append(review_obj)

#     return results

def analyze_review_sentiments(dealerreview):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/e9647bb4-2918-4acd-9d51-84c7ce9ef927"
    api_key = "WkMOfDRpUnFF9msEm2NZKeamAvGIc73AixHz0dKifuMv"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=dealerreview,features=Features(sentiment=SentimentOptions(targets=[dealerreview]))).get_result()
    label = response['sentiment']['document']['label']
    
    return(label)

def post_request(url, json_payload, **kwargs):
    print("Payload: ", json_payload, ". Params: ", kwargs)
    print(f"POST {url}")
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                 json=json_payload, params=kwargs)
        response.raise_for_status()  # Raise HTTPError for bad requests
    except requests.exceptions.RequestException as e:
        # Handle specific request-related exceptions
        print("Request exception occurred:", e)
        return {"error": str(e)}
    except Exception as e:
        # Handle other exceptions
        print("Exception occurred:", e)
        return {"error": "An unexpected error occurred"}

    status_code = response.status_code
    print("With status {} ".format(status_code))
    
    try:
        json_data = response.json()  # Try to parse response as JSON
    except json.JSONDecodeError:
        print("Failed to parse response as JSON")
        return {"error": "Failed to parse response as JSON"}
    
    return json_data
















# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative




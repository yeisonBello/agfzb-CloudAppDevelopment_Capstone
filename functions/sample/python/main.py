"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict):
  
    try:
        # Connect to the Cloudant database
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )

        # Get a specific database (replace 'reviews' with your actual database name)
        database = client['reviews']

        # Retrieve reviews for the specified dealerId
        dealer_id = param_dict.get("dealerId")
        reviews = []
        for document in database:
            if document.get("id") == dealer_id:
                reviews.append(document)  # Assuming each document in the 'reviews' database represents a review for a specific dealerId

        # If no reviews found, return 404 error
        if not reviews:
            return {"error": "DealerId does not exist"}, 404

        # Return the list of reviews for the specified dealership
        return {"reviews": reviews}

    
    except CloudantException as cloudant_exception:
        print("Error connecting to the database")
        return {"error": "Something went wrong on the server"}, 500
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("Connection error")
        return {"error": "Something went wrong on the server"}, 500

    finally:
        # Always remember to disconnect from the database after the operation
        client.disconnect()



def post_review(param_dict):
    """Function to post a review for a dealership"""

    try:
        # Connect to the Cloudant database
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )

        # Get a specific database (replace 'reviews' with your actual database name)
        database = client['reviews']

        # Extract review data from the request parameters
        review_data = param_dict.get("review")
        dealer_id = review_data.get("dealership")
        
        # Check if the dealership exists
        if not get_reviews(dealer_id, database):
            return {"error": "DealerId does not exist"}, 404

        # Insert the review into the database
        document = database.create_document(review_data)

        # Return success response
        return {"message": "Review posted successfully", "reviewId": document["_id"]}, 201  # 201 Created status code

    except CloudantException as cloudant_exception:
        print("Error connecting to the database")
        return {"error": "Something went wrong on the server"}, 500
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("Connection error")
        return {"error": "Something went wrong on the server"}, 500

    finally:
        # Always remember to disconnect from the database after the operation
        client.disconnect()

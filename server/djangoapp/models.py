from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
  name = models.CharField(null=False, max_length=30, default='car')
  description = models.CharField(null=False, max_length=60, default='sport car')

 # def __str__(self):
 #       return self.name + " " + self.description
  def __str__(self):
        return self.name 

class CarModel(models.Model):
   CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'WAGON'),
    ]
   car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
   dealer_id = models.IntegerField()  # Assuming this is an ID from the Cloudant database
   name = models.CharField(null=False, max_length=30, default='carmake')
   type = models.CharField(max_length=10, choices=CAR_TYPES)
   year = models.DateField()
    # Add any other fields you want for CarModel model
    
   def __str__(self):
        return f"{self.car_make.name} - {self.name}"
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
        def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
            # Dealer address
            self.address = address
            # Dealer city
            self.city = city
            # Dealer Full Name
            self.full_name = full_name
            # Dealer id
            self.id = id
            # Location lat
            self.lat = lat
            # Location long
            self.long = long
            # Dealer short name
            self.short_name = short_name
            # Dealer state
            self.st = st
            # Dealer zip
            self.zip = zip
        def __str__(self):
            return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self, sentiment, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year,  id):
        # Dealership object (instance of CarDealer class)
        self.dealership = dealership
        # Reviewer's name
        self.name = name
        # Whether the review is based on a purchase or not
        self.purchase = purchase
        # Review text
        self.review = review
        # Date of purchase
        self.purchase_date = purchase_date
        # Car make (e.g., Toyota, Ford)
        self.car_make = car_make
        # Car model (e.g., Camry, Mustang)
        self.car_model = car_model
        # Car year (e.g., 2022)
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    

    def __str__(self):
        return f"Review for {self.dealership.full_name} by {self.name} on {self.review_date}: {self.review}"


import csv
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #prevents some warnings
# db = SQLAlchemy(app)
# Bootstrap(app)
import model

import views

# class Restaurant(db.Model):
#     # Data schema for restaurant data / table
#     __tablename__ = "restaurants"
#     id = db.Column(db.Integer, primary_key=True)
#     restaurantName = db.Column(db.String(250), nullable=False)
#     serviceType = db.Column(db.String(100), nullable=False)
#     cuisineType = db.Column(db.String(100), nullable=False)
#     reviews = relationship("Review", back_populates="")
#
# class Review(db.Model):
#     # Data schema for restaurant data / table
#     __tablename__ = "reviews"
#     reviewID = db.Column(db.Integer, primary_key=True)
#     restaurantID = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
#     restaurant = relationship("Restaurant", back_populates="reviews")
#     bestSuitedFor = db.Column(db.String, nullable=False)
#     diningOptions = db.Column(db.String, nullable=False)
#     expensePerHead = db.Column(db.Integer, nullable=False)
#     foodQuality = db.Column(db.Integer, nullable=False)
#     ambiance = db.Column(db.Integer, nullable=False)
#     serviceQuality = db.Column(db.Integer, nullable=False)
#     cleanliness = db.Column(db.Integer, nullable=False)
#     speedOfService = db.Column(db.Integer, nullable=False)
#     valueForMoney = db.Column(db.Integer, nullable=False)
#     allergyInfoProvided = db.Column(db.String, nullable=False)
#     overallRating = db.Column(db.String, nullable=False)
#     comments = db.Column(db.String, nullable=False)

# db.create_all()

@app.route('/download')
def downloadReport():
    # For use by the newspaper to download all DB entries in a CSV file for them to do further analysis.
    path = "RestaurantData.csv"
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Review_ID', 'Restaurant', 'Service_Type', 'Cuisine', 'Suited_For',
                                                    'Dining_Options', 'Cost_PerHead', 'Food_Quality', 'Ambiance', 'Service_Quality', 'Cleanliness',
                                                    'Speed_OfService', 'Value_ForMoney', 'Allergy_InfoProvided', 'Overall_Rating', 'Comments'])
        writer.writeheader()
        for row in db.session.query(Review).all():
            row_data = {
                'Review_ID': row.reviewID,
                'Restaurant': row.restaurant.restaurantName,
                'Service_Type': row.restaurant.serviceType,
                'Cuisine': row.restaurant.cuisineType,
                'Suited_For': row.bestSuitedFor,
                'Dining_Options': row.diningOptions,
                'Cost_PerHead': row.expensePerHead,
                'Food_Quality': row.foodQuality,
                'Ambiance': row.ambiance,
                'Service_Quality': row.serviceQuality,
                'Cleanliness': row.cleanliness,
                'Speed_OfService': row.speedOfService,
                'Value_ForMoney': row.valueForMoney,
                'Allergy_InfoProvided': row.allergyInfoProvided,
                'Overall_Rating': row.overallRating,
                'Comments': row.comments
            }
            writer.writerow(row_data)
    return send_file(path, as_attachment=True) #serves CSV to the user as browser download.

# def addRestaurant(name, serviceType, cuisineType):
#     # Adds new restaurant to Database
#     new_restaurant = Restaurant(
#         restaurantName=name,
#         serviceType=serviceType,
#         cuisineType=cuisineType,
#     )
#     db.session.add(new_restaurant)
#     db.session.commit()

# def addReview(restaurantName,suitedfor,diningoptions,expense,quality, ambiance,servicequality,cleanliness, speed, value, allergyinfo, overallrating, comments):
#     # Adds new review to database, linked with an existing restaurant.
#     restaurant = db.session.query(Restaurant).filter_by(restaurantName=restaurantName).first()
#     new_review = Review(
#         restaurant=restaurant,
#         bestSuitedFor = suitedfor,
#         diningOptions = diningoptions,
#         expensePerHead = expense,
#         foodQuality = quality,
#         ambiance = ambiance,
#         serviceQuality = servicequality,
#         cleanliness = cleanliness,
#         speedOfService = speed,
#         valueForMoney = value,
#         allergyInfoProvided = allergyinfo,
#         overallRating = overallrating,
#         comments = comments
#     )
#     db.session.add(new_review)
#     db.session.commit()

# def setupTestRestaurants():
#     # If no restaurants exist in the database, 3 test restaurants will be created to help testing.
#     existingrestaurants = db.session.query(Restaurant).all()
#     if not existingrestaurants:
#         testrestaurants = [{"name": "Benny's Italian", "serviceType": "Takeaway", "cuisine": "Italian"}, {"name": "Le Mariners", "serviceType": "Fine Dining", "cuisine": "French"}, {"name": "Wendy's Diner", "serviceType": "Casual", "cuisine": "American"}]
#         for restaurant in testrestaurants:
#             addRestaurant(restaurant["name"], restaurant["serviceType"], restaurant["cuisine"])

# def setupTestReviews():
#     # If no reviews exist in the database, 6 test reviews will be created to help testing.
#     existingreviews = db.session.query(Review).all()
#     if not existingreviews:
#         testreviews = [
#             {"restaurantName": "Benny's Italian", "suitedfor": "Couples", "diningoptions": "Dinner", "expense": 4, "quality": 4, "ambiance": 2, "servicequality": 1, "cleanliness": 4, "speed": 5, "value": 2, "allergyinfo": "Yes", "overallrating": "Poor", "comments": "fine"},
#             {"restaurantName": "Benny's Italian", "suitedfor": "Couples", "diningoptions": "Dinner", "expense": 3, "quality": 3, "ambiance": 1, "servicequality": 1, "cleanliness": 4, "speed": 5, "value": 4, "allergyinfo": "Yes", "overallrating": "Good", "comments": "Not bad"},
#             {"restaurantName": "Benny's Italian", "suitedfor": "Kids", "diningoptions": "Dinner", "expense": 1, "quality": 1,
#              "ambiance": 1, "servicequality": 1, "cleanliness": 1, "speed": 1, "value": 1, "allergyinfo": "Yes",
#              "overallrating": "Good", "comments": "Horrid"},
#             {"restaurantName": "Le Mariners", "suitedfor": "Families", "diningoptions": "Dinner", "expense": 4, "quality": 4,
#              "ambiance": 2, "servicequality": 1, "cleanliness": 4, "speed": 5, "value": 2, "allergyinfo": "Yes",
#              "overallrating": "Poor", "comments": "Amazing!!"},
#             {"restaurantName": "Wendy's Diner", "suitedfor": "Weddings", "diningoptions": "Dinner", "expense": 4, "quality": 4,
#              "ambiance": 2, "servicequality": 1, "cleanliness": 4, "speed": 5, "value": 2, "allergyinfo": "Yes",
#              "overallrating": "Excellent", "comments": "fine"},
#             {"restaurantName": "Le Mariners", "suitedfor": "Couples", "diningoptions": "Dinner", "expense": 5, "quality": 5,
#              "ambiance": 5, "servicequality": 5, "cleanliness": 5, "speed": 5, "value": 5, "allergyinfo": "No",
#              "overallrating": "Excellent", "comments": "My favourite"},
#         ]
#         for review in testreviews:
#             addReview(review["restaurantName"], review["suitedfor"], review["diningoptions"],review["expense"],review["quality"],review["ambiance"],review["servicequality"],review["cleanliness"],review["speed"],review["value"],review["allergyinfo"], review["overallrating"], review["comments"])

model.setupTestRestaurants()
model.setupTestReviews()
# setupTestRestaurants()
# setupTestReviews()
# downloadReport()

# @app.route('/')
# def home():
#     return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)
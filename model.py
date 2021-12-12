from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, load_only
from flask import jsonify
from __main__ import app

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #prevents some warnings
db = SQLAlchemy(app)

#Data for drop down selections - dummy at the mo - will need replacing once we determine what options we want for final.
serviceTypes = ["A La Carte", "Buffet", "Cafe", "Fast Food", "Fine Dining", "Food Truck / Street Food", "Pub", "Takeaway", "Other"]
cuisineTypes = ['American', 'Asian', 'Caribbean', 'English', 'French', 'Italian', 'Middle Eastern', 'Vegan', 'Other']
occasionTypes = ['Business Lunch', 'Family Meal', 'Kids', 'Romantic Meal', 'Scenic Views', 'Special Events', 'Other']
mealOptions = ['Breakfast', 'Brunch', 'Lunch', 'Dinner', 'Late Night', 'Other', 'Multiple']
#Test data - not needed when testing for real
testrestaurants = [{"name": "Benny's Italian", "serviceType": "Takeaway", "cuisine": "Italian", "diningOptions": "Dinner"}, {"name": "Le Mariners", "serviceType": "Fine Dining", "cuisine": "French", "diningOptions": "Dinner",}, {"name": "Wendy's Diner", "serviceType": "Casual", "cuisine": "American", "diningOptions": "Dinner",}]
testreviews = [
    {"restaurantName": "Benny's Italian", "suitedfor": "Couples",  "expense": 4, "quality": 4,
     "ambiance": 2, "servicequality": 1, "cleanliness": 4, "speed": 5, "value": 2, "allergyinfo": 3,
     "overallrating": 5, "comments": "fine"},
    {"restaurantName": "Benny's Italian", "suitedfor": "Couples", "expense": 3, "quality": 3,
     "ambiance": 1, "servicequality": 1, "cleanliness": 4, "speed": 5, "value": 4, "allergyinfo": 3,
     "overallrating": 5, "comments": "Not bad"},
    {"restaurantName": "Benny's Italian", "suitedfor": "Kids", "expense": 1, "quality": 1,
     "ambiance": 1, "servicequality": 1, "cleanliness": 1, "speed": 1, "value": 1, "allergyinfo": 3,
     "overallrating": 3, "comments": "Horrid"},
    {"restaurantName": "Le Mariners", "suitedfor": "Families", "expense": 4, "quality": 4,
     "ambiance": 2, "servicequality": 1, "cleanliness": 4, "speed": 5, "value": 2, "allergyinfo": 3,
     "overallrating": 2, "comments": "Amazing!!"},
    {"restaurantName": "Wendy's Diner", "suitedfor": "Weddings", "expense": 4, "quality": 4,
     "ambiance": 2, "servicequality": 1, "cleanliness": 4, "speed": 5, "value": 2, "allergyinfo": 3,
     "overallrating": 1, "comments": "fine"},
    {"restaurantName": "Le Mariners", "suitedfor": "Couples", "expense": 5, "quality": 5,
     "ambiance": 5, "servicequality": 5, "cleanliness": 5, "speed": 5, "value": 5, "allergyinfo": 3,
     "overallrating": 1, "comments": "My favourite"},
]

# Class schemas for database
class MealType(db.Model):
    __tablename__ = "diningoptions"
    id = db.Column(db.Integer, primary_key=True)
    mealOption = db.Column(db.String, nullable=False)

class Occasion(db.Model):
    __tablename__ = "diningoccasions"
    id = db.Column(db.Integer, primary_key=True)
    diningOccasion = db.Column(db.String, nullable=False)

class Cuisine(db.Model):
    __tablename__ = "cuisines"
    id = db.Column(db.Integer, primary_key=True)
    cuisine = db.Column(db.String, nullable=False)

class ServiceType(db.Model):
    __tablename__ = "servicetypes"
    id = db.Column(db.Integer, primary_key=True)
    serviceType = db.Column(db.String, nullable=False)

class Restaurant(db.Model):
    # Data schema for restaurant data / table
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    restaurantName = db.Column(db.String(250), nullable=False, unique=True)
    serviceType = db.Column(db.String(100), nullable=False)
    cuisineType = db.Column(db.String(100), nullable=False)
    diningOptions = db.Column(db.String, nullable=False)
    avgExpense = db.Column(db.Integer, nullable=False)
    avgFoodQuality = db.Column(db.Integer, nullable=False)
    avgAmbiance = db.Column(db.Integer, nullable=False)
    avgServiceQuality = db.Column(db.Integer, nullable=False)
    avgCleanliness = db.Column(db.Integer, nullable=False)
    avgSpeedOfService = db.Column(db.Integer, nullable=False)
    avgValueForMoney = db.Column(db.Integer, nullable=False)
    avgAllergyInfoQuality = db.Column(db.Integer, nullable=False)
    avgOverallRating = db.Column(db.Integer, nullable=False)
    reviews = relationship("Review", back_populates="")

    def to_dict(self):
        # Converts the chosen database entry item into a Dictionary item that can be converted to JSON easier than writing in each key / value
        dictionary = {}
        for column in self.__table__.columns:
            #Creates the dictionary item where the key is the name of the column and the value is the value in the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

class Review(db.Model):
    # Data schema for restaurant data / table
    __tablename__ = "reviews"
    reviewID = db.Column(db.Integer, primary_key=True)
    restaurantID = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = relationship("Restaurant", back_populates="reviews")
    bestSuitedFor = db.Column(db.String, nullable=False)
    expensePerHead = db.Column(db.Integer, nullable=False)
    foodQuality = db.Column(db.Integer, nullable=False)
    ambiance = db.Column(db.Integer, nullable=False)
    serviceQuality = db.Column(db.Integer, nullable=False)
    cleanliness = db.Column(db.Integer, nullable=False)
    speedOfService = db.Column(db.Integer, nullable=False)
    valueForMoney = db.Column(db.Integer, nullable=False)
    allergyInfoProvided = db.Column(db.Integer, nullable=False)
    overallRating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String, nullable=False)

    def to_dict(self):
        # Converts the chosen database entry item into a Dictionary item that can be converted to JSON easier than writing in each key / value
        dictionary = {}
        for column in self.__table__.columns:
            #Creates the dictionary item where the key is the name of the column and the value is the value in the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

db.create_all()


# FUNCTIONS TO ADD DATA TO DATABASE
def addRestaurant(name, serviceType, cuisineType, diningOptions):
    # Adds new restaurant to Database
    new_restaurant = Restaurant(
        restaurantName=name,
        serviceType=serviceType,
        cuisineType=cuisineType,
        diningOptions=diningOptions,
        avgExpense = 0,
        avgFoodQuality = 0,
        avgAmbiance = 0,
        avgServiceQuality = 0,
        avgCleanliness = 0,
        avgSpeedOfService = 0,
        avgValueForMoney = 0,
        avgAllergyInfoQuality = 0,
        avgOverallRating = 0
    )
    db.session.add(new_restaurant)
    db.session.commit()

def addReview(restaurantID,suitedfor,expense,quality, ambiance,servicequality,cleanliness, speed, value, allergyinfo, overallrating, comments):
    # 1. Adds new review to database, linked with an existing restaurant.
    restaurant = db.session.query(Restaurant).filter_by(id=restaurantID).first()
    new_review = Review(
        restaurant=restaurant,
        bestSuitedFor = suitedfor,
        expensePerHead = expense,
        foodQuality = quality,
        ambiance = ambiance,
        serviceQuality = servicequality,
        cleanliness = cleanliness,
        speedOfService = speed,
        valueForMoney = value,
        allergyInfoProvided = allergyinfo,
        overallRating = overallrating,
        comments = comments
    )
    db.session.add(new_review)
    db.session.commit()
    # 2. Calculate and update restaurant average scores, including the new review
    restaurant_to_update = db.session.query(Restaurant).filter_by(id=restaurantID).first()
    avgExpense = 0
    avgFoodQuality = 0
    avgAmbiance = 0
    avgServiceQuality = 0
    avgCleanliness = 0
    avgSpeedOfService = 0
    avgValueForMoney = 0
    avgAllergyInfoQuality = 0
    avgOverallRating = 0
    reviewNumber = len(restaurant_to_update.reviews)
    for review in restaurant_to_update.reviews:
        avgExpense += review.expensePerHead
        avgFoodQuality += review.foodQuality
        avgAmbiance += review.ambiance
        avgServiceQuality += review.serviceQuality
        avgCleanliness += review.cleanliness
        avgSpeedOfService += review.speedOfService
        avgValueForMoney += review.valueForMoney
        avgAllergyInfoQuality += review.allergyInfoProvided
        avgOverallRating += review.overallRating
    restaurant_to_update.avgExpense = round(avgExpense / reviewNumber)
    restaurant_to_update.avgFoodQuality = round(avgFoodQuality / reviewNumber)
    restaurant_to_update.avgAmbiance = round(avgAmbiance / reviewNumber)
    restaurant_to_update.avgServiceQuality = round(avgServiceQuality / reviewNumber)
    restaurant_to_update.avgCleanliness = round(avgCleanliness / reviewNumber)
    restaurant_to_update.avgSpeedOfService = round(avgSpeedOfService / reviewNumber)
    restaurant_to_update.avgValueForMoney = round(avgValueForMoney / reviewNumber)
    restaurant_to_update.avgAllergyInfoQuality = round(avgAllergyInfoQuality / reviewNumber)
    restaurant_to_update.avgOverallRating = round(avgOverallRating / reviewNumber)
    db.session.commit()


def addSingleDBOption(type, option):
    if type == "service":
        new_option = ServiceType(serviceType=option)
    elif type == "occasion":
        new_option = Occasion(diningOccasion=option)
    elif type == "cuisine":
        new_option = Cuisine(cuisine=option)
    elif type == "diningoption":
        new_option = MealType(mealOption=option)
    db.session.add(new_option)
    db.session.commit()

# FUNCTIONS TO RETURN DATA FROM DATABASE
def returnDatabaseColumnData(table, column):
    #Returns specific column from table - i.e. to populate drop down lists
    return db.session.query(table).options(load_only(column)).all()

def returnDatabaseData(table):
    #Returns entire table
    return db.session.query(table).all()


# API FUNCTIONS
def APISearch(restaurantname="", cuisine="", cost="", occasion=""):
    # Searches data to find restaurants that match search criteria
    restaurantIDs = []
    filters = []
    if restaurantname:
        # filters.append(Restaurant.restaurantName.like(restaurantname))
        filters.append(Restaurant.restaurantName.contains(restaurantname))
    if cuisine:
        filters.append(Restaurant.cuisineType.contains(cuisine))
    if cost:
        filters.append(Restaurant.avgExpense==cost)
    if occasion:
        # Slightly different logic - get reviews that have the recommended occasion type and then work back to get the restaurants where people have recommended for
        reviews = db.session.query(Review).filter(Review.bestSuitedFor==occasion).distinct(Review.restaurant).all()
        for review in reviews:
            restaurantIDs.append(review.restaurant.id)
        filters.append(Restaurant.id.in_(restaurantIDs))
    restaurants = db.session.query(Restaurant).filter(*filters).order_by(Restaurant.avgOverallRating.desc()).all()
    return jsonify(results=[restaurant.to_dict() for restaurant in restaurants])  # Creates a dictionary item for each within the same JSON

def returnRestaurant(id):
    restaurants = db.session.query(Restaurant).filter(Restaurant.id == id).all()
    return jsonify(results=[restaurant.to_dict() for restaurant in restaurants])  # Creates a dictionary item for each within the same JSON

def returnReviews(id):
    reviews = db.session.query(Review).filter(Review.restaurantID == id).all()
    return jsonify(results=[review.to_dict() for review in reviews])  # Creates a dictionary item for each within the same JSON


# FUNCTIONS TO CREATE DUMMY DATA IN TABLES FOR TESTING
def setupTestRestaurants():
    # If no restaurants exist in the database, 3 test restaurants will be created to help testing.
    existingrestaurants = returnDatabaseColumnData(Restaurant, "restaurantName")
    if not existingrestaurants:
        for restaurant in testrestaurants:
            addRestaurant(name=restaurant["name"], serviceType=restaurant["serviceType"], cuisineType=restaurant["cuisine"], diningOptions=restaurant["diningOptions"])

def setupTestReviews():
    # If no reviews exist in the database, 6 test reviews will be created to help testing.
    existingreviews = db.session.query(Review).all()
    if not existingreviews:
        for review in testreviews:
            addReview(review["restaurantName"], review["suitedfor"], review["expense"],review["quality"],review["ambiance"],review["servicequality"],review["cleanliness"],review["speed"],review["value"],review["allergyinfo"], review["overallrating"], review["comments"])

def setupOtherData():
    existingservicetypes = returnDatabaseColumnData(ServiceType, "serviceType")
    if not existingservicetypes:
        for service in serviceTypes:
            addSingleDBOption("service", service)
    existingcuisinetypes = returnDatabaseColumnData(Cuisine, "cuisine")
    if not existingcuisinetypes:
        for cuisine in cuisineTypes:
            addSingleDBOption("cuisine", cuisine)
    existingoccassontypes = returnDatabaseColumnData(Occasion, "diningOccasion")
    if not existingoccassontypes:
        for occasion in occasionTypes:
            addSingleDBOption("occasion", occasion)
    existingmealtypes = returnDatabaseColumnData(MealType, "mealOption")
    if not existingmealtypes:
        for meal in mealOptions:
            addSingleDBOption("diningoption", meal)

def testingInit():
    # Single function to run the other test / setup functions.
    setupTestRestaurants()
    setupTestReviews()
    setupOtherData()



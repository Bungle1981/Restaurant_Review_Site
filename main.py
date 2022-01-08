import csv
from flask import Flask, render_template, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, load_only

app = Flask(__name__)
app.config["DEBUG"] = True
csvPath = "RestaurantData.csv"

# MODEL CODE - ORIGINALLY IN A SEPARATE MODULE BUT HEROKU DOESN'T SEEM TO LIKE THIS
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db" #Not the best for Heroku but constant issues trying other routes - now worth the hassle purely for testing.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #prevents some warnings
db = SQLAlchemy(app)

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


# ORIGINAL MAIN.PY CONTENT - API ROUTES AND FUNCTIONS
def createCSV():
    # Function to create CSV file from reviews
    with open(csvPath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Review_ID', 'Restaurant', 'Service_Type', 'Cuisine', 'Suited_For',
                                                    'Dining_Options', 'Cost_PerHead', 'Food_Quality', 'Ambiance', 'Service_Quality', 'Cleanliness',
                                                    'Speed_OfService', 'Value_ForMoney', 'Allergy_InfoProvided', 'Overall_Rating', 'Comments'])
        writer.writeheader()
        for row in returnDatabaseData(Review):
            row_data = {
                'Review_ID': row.reviewID,
                'Restaurant': row.restaurant.restaurantName,
                'Service_Type': row.restaurant.serviceType,
                'Cuisine': row.restaurant.cuisineType,
                'Suited_For': row.bestSuitedFor,
                'Dining_Options': row.restaurant.diningOptions,
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

# API ROUTES
@app.route('/search', methods=['GET'])
def api_RestaurantSearch():
    # API Route for restaurant searches
    name = request.args.get('name')
    cuisine = request.args.get('cuisine')
    cost = request.args.get('cost')
    occasion = request.args.get('occasion')
    response = APISearch(restaurantname=name, cuisine=cuisine, cost=cost, occasion=occasion)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/restaurantinfo', methods=['GET', 'POST'])
def api_RestaurantInfo():
    # API Route to get restaurant info with known ID or to add new restaurant to DB
    if request.method == "GET":
        response = returnRestaurant(id=request.args.get('id'))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    elif request.method == "POST":
        requestData = request.get_json(force=True)
        restaurantName = str(requestData.get('restaurantName'))
        serviceType = str(requestData.get('service'))
        cuisineType = str(requestData.get('cuisine'))
        diningOptions = str(requestData.get('diningOptions'))
        addRestaurant(
            name=restaurantName,
            serviceType=serviceType,
            cuisineType=cuisineType,
            diningOptions=diningOptions
        )
        response = APISearch(restaurantname=restaurantName)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/getreviews', methods=['GET'])
def api_GetReviews():
    response = returnReviews(request.args.get('id'))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/addreview', methods=['POST'])
def api_AddReview():
    if request.method == "POST":
        requestData = request.get_json(force=True)
        restaurantID = int(requestData.get('restaurantID'))
        suitedfor = str(requestData.get('bestSuitedFor'))
        expense = int(requestData.get('expensePerHead'))
        quality = int(requestData.get('foodQuality'))
        ambiance = int(requestData.get('ambiance'))
        servicequality = int(requestData.get('serviceQuality'))
        cleanliness = int(requestData.get('cleanliness'))
        speed = int(requestData.get('speedOfService'))
        value = int(requestData.get('valueForMoney'))
        allergyinfo = int(requestData.get('allergyInfoProvided'))
        overallrating = int(requestData.get('overallRating'))
        comments = str(requestData.get('comments'))
        addReview(
            restaurantID=restaurantID,
            suitedfor=suitedfor,
            expense = expense,
            quality = quality,
            ambiance=ambiance,
            servicequality=servicequality,
            cleanliness=cleanliness,
            speed=speed,
            value=value,
            allergyinfo = allergyinfo,
            overallrating = overallrating,
            comments=comments
        )
        # Return new restaurant data
        response = returnRestaurant(id=restaurantID)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

# NON-API ROUTES
@app.route('/', methods=["GET"])
def homePage():
    # Loads drop down values and renders them to the search page
    return render_template("Index.html", restaurants=returnDatabaseColumnData(Restaurant, "restaurantName"), occasions=returnDatabaseColumnData(Occasion, "diningOccasion"), cuisines=returnDatabaseColumnData(Cuisine, "cuisine"), services=returnDatabaseColumnData(ServiceType, "serviceType"), mealtypes=returnDatabaseColumnData(MealType, "mealOption"))

@app.route('/admin', methods=['GET'])
def adminRoute():
    # Renders admin page
    return render_template("Admin.html")

@app.route('/download', methods=['GET'])
def downloadCSV():
    # For use by the newspaper to download all DB entries in a CSV file for them to do further analysis.
    createCSV()
    return send_file(csvPath, as_attachment=True) # Serves CSV to the user as browser download.

if __name__ == "__main__":
    app.run(debug=True)
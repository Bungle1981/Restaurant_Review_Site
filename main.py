import csv
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify, Response
import json

app = Flask(__name__)
# from flask_bootstrap import Bootstrap
# Bootstrap(app)
import model
csvPath = "RestaurantData.csv"

def createCSV():
    with open(csvPath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Review_ID', 'Restaurant', 'Service_Type', 'Cuisine', 'Suited_For',
                                                    'Dining_Options', 'Cost_PerHead', 'Food_Quality', 'Ambiance', 'Service_Quality', 'Cleanliness',
                                                    'Speed_OfService', 'Value_ForMoney', 'Allergy_InfoProvided', 'Overall_Rating', 'Comments'])
        writer.writeheader()
        for row in model.returnDatabaseData(model.Review):
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
    # print(f"name: {name}\ncuisine: {cuisine}\ncost: {cost}\noccasion: {occasion}")
    response = model.APISearch(restaurantname=name, cuisine=cuisine, cost=cost, occasion=occasion)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/restaurantinfo', methods=['GET', 'POST'])
def api_RestaurantInfo():
    # API Route to get restaurant info with known ID or to add new restaurant to DB
    if request.method == "GET":
        response = model.returnRestaurant(id=request.args.get('id'))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    elif request.method == "POST":
        requestData = request.get_json(force=True)
        restaurantName = str(requestData.get('restaurantName'))
        serviceType = str(requestData.get('service'))
        cuisineType = str(requestData.get('cuisine'))
        diningOptions = str(requestData.get('diningOptions'))
        model.addRestaurant(
            name=restaurantName,
            serviceType=serviceType,
            cuisineType=cuisineType,
            diningOptions=diningOptions
        )
        response = model.APISearch(restaurantname=restaurantName)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/getreviews', methods=['GET'])
def api_GetReviews():
    response = model.returnReviews(request.args.get('id'))
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
        model.addReview(
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
        response = model.returnRestaurant(id=restaurantID)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


# NON-API ROUTES

@app.route('/', methods=["GET"])
def homePage():
    # # Loads drop down values and renders them to the search page
    return render_template("Index.html", restaurants=model.returnDatabaseColumnData(model.Restaurant, "restaurantName"), occasions=model.returnDatabaseColumnData(model.Occasion, "diningOccasion"), cuisines=model.returnDatabaseColumnData(model.Cuisine, "cuisine"), services=model.returnDatabaseColumnData(model.ServiceType, "serviceType"), mealtypes=model.returnDatabaseColumnData(model.MealType, "mealOption"))


@app.route('/admin', methods=['GET', 'POST'])
def adminRoute():
    if request.method == "POST":
        # Placeholder for getting admin access and returning the CSV
        downloadCSV()
    else:
        return render_template("adminLogin.html")

@app.route('/download', methods=['GET'])
def downloadCSV():
    # For use by the newspaper to download all DB entries in a CSV file for them to do further analysis.
    createCSV()
    return send_file(csvPath, as_attachment=True) # Serves CSV to the user as browser download.



# Create test restaurants/reviews ready for testing if no data in database
model.testingInit()

if __name__ == "__main__":
    app.run(debug=True)
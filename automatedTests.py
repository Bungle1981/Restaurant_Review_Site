# THIS MODULE USES SELENIUM TO CONTROL GOOGLE CHROME AND RUN AUTOMATED TESTS ON THE HEROKU HOSTED VERSION OF THE SITE.
from selenium import webdriver
import csv
from time import sleep
import random

MAIN_WEBSITE_URL = "https://restaurantreview-site.herokuapp.com/"
restaurantNames = ["London", 'Capel St Mary', "Prince's Street", 'Colchester', 'Braintree']
restaurantTypes = ['Cafe', 'Diner', 'Bistro', 'Canteen', 'Eatery', 'Chinese', 'Cottage', 'Indian', 'Buffet', 'Kitchen']
cuisineTypes = ['American', 'Asian', 'Caribbean', 'English', 'French', 'Italian', 'Middle Eastern', 'Vegan', 'Other']
serviceTypes = ['A La Carte', 'Buffet', 'Cafe', 'Fast Food', 'Fine Dining', 'Food Truck / Street Food', 'Pub', 'Takeaway', 'Other']
mealTypes = ['Breakfast', 'Brunch', 'Lunch', 'Dinner', 'Late Night', 'Other', 'Multiple']
occasionTypes = ['Business Lunch', 'Family Meal', 'Kids', 'Romantic Meal', 'Scenic Views', 'Special Events', 'Other']
costPerHead = ['£', '££', '£££', '££££', '£££££']
otherDropDown = ['Terrible', 'Poor', 'Average', 'Very good', 'Excellent']
csvPath = "automatedTestResults.csv"
testNumber = 1

# Set up Selenium and navigate to site
chrome_driver_path = "C:\Program Files\ChromeDriver\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(MAIN_WEBSITE_URL)

# Open CSV, ready to start writing test results to file (File closes automatically once tests are finished)
with open(csvPath, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['Test_ID', 'Test_Description', 'Test_Result'])
    writer.writeheader()

    # Test 1: Is page title correct in browser?
    row_data = {
        'Test_ID': testNumber,
        'Test_Description': 'Is the browser window correctly titled `Restaurant Review Site`?',
        'Test_Result': 'Pass' if driver.title == "Restaurant Review Site" else 'Fail'
    }
    writer.writerow(row_data)
    testNumber += 1

    # Test 2+: Add Restaurants, with 2 reviews each
    for name in restaurantNames:
        for type in restaurantTypes:
            # Set unique generated restaurant details
            restaurantName = f"{name} {type}"
            restaurantCuisine = random.choice(cuisineTypes)
            restaurantService = random.choice(serviceTypes)
            restaurantMeal = random.choice(mealTypes)
            # Search for restaurant
            driver.find_element_by_id("restaurantSearch").send_keys(restaurantName)
            driver.find_element_by_id("searchButton").click()
            sleep(0.5)
            # Add details of generated restaurant to site
            driver.find_element_by_id("addRestaurantButton").click()
            driver.find_element_by_id("restaurantNameInput").send_keys(restaurantName)
            driver.find_element_by_xpath(f"//*[@id='cuisineInput-dropdown']/option[text()='{restaurantCuisine}']").click()
            driver.find_element_by_xpath(f"//*[@id='serviceInput-dropdown']/option[text()='{restaurantService}']").click()
            driver.find_element_by_xpath(f"//*[@id='diningOptionsInput-dropdown']/option[text()='{restaurantMeal}']").click()
            driver.find_element_by_id("restaurantSubmitButton").click()
            sleep(0.5)
            # Check to see if restaurant is added
            searchedName = driver.find_elements_by_class_name("search-result-preview")[0].find_element_by_tag_name("h3").text
            searchedScore = driver.find_elements_by_class_name("search-result-preview")[0].find_element_by_tag_name("p").text
            infoName = driver.find_element_by_id("restaurantNameHeading").text
            # Write result of adding restaurant test to CSV
            row_data = {
                'Test_ID': testNumber,
                'Test_Description': f"'{restaurantName}' restaurant added to site?",
                'Test_Result': 'Pass' if searchedName == restaurantName and infoName == restaurantName and searchedScore == "Average rating: 0 / 5" else 'Fail'
            }
            writer.writerow(row_data)
            testNumber += 1
            # Leave 2 reviews to new restaurant
            for x in range(2):
                # Set review text so unique to review 1 and review 2
                reviewText = f"Review {x + 1}"
                # Select random drop down selections on review page
                driver.find_element_by_id("reviewThisRestaurantButton").click()
                driver.find_element_by_xpath(f"//*[@id='occasions-dropdown']/option[text()='{random.choice(occasionTypes)}']").click()
                driver.find_element_by_xpath(f"//*[@id='expense-dropdown']/option[text()='{random.choice(costPerHead)}']").click()
                driver.find_element_by_xpath(f"//*[@id='foodQuality-dropdown']/option[text()='{random.choice(otherDropDown)}']").click()
                driver.find_element_by_xpath(f"//*[@id='ambiance-dropdown']/option[text()='{random.choice(otherDropDown)}']").click()
                driver.find_element_by_xpath(f"//*[@id='customerService-dropdown']/option[text()='{random.choice(otherDropDown)}']").click()
                driver.find_element_by_xpath(f"//*[@id='cleanliness-dropdown']/option[text()='{random.choice(otherDropDown)}']").click()
                driver.find_element_by_xpath(f"//*[@id='speedofservice-dropdown']/option[text()='{random.choice(otherDropDown)}']").click()
                driver.find_element_by_xpath(f"//*[@id='valueForMoney-dropdown']/option[text()='{random.choice(otherDropDown)}']").click()
                driver.find_element_by_xpath(f"//*[@id='allergy-dropdown']/option[text()='{random.choice(otherDropDown)}']").click()
                driver.find_element_by_xpath(f"//*[@id='overallRating-dropdown']/option[text()='{random.choice(otherDropDown)}']").click()
                # Add review comments
                driver.find_element_by_id("reviewComments").send_keys(reviewText)
                # Submit review and wait for page to refresh
                driver.find_element_by_id("consent-checkbox").click()
                driver.find_element_by_id("reviewSubmitButton").click()
                sleep(0.5)
                # Write result of adding review test to CSV
                savedReview = driver.find_elements_by_class_name("comment-box")[x].find_element_by_tag_name("p").text
                row_data = {
                    'Test_ID': testNumber,
                    'Test_Description': f"'{restaurantName}' restaurant '{reviewText}' added to site?",
                    'Test_Result': 'Pass' if savedReview == reviewText else 'Fail'
                }
                writer.writerow(row_data)
                testNumber += 1

# All tests run, close Browser
driver.close()
"use strict";

// Variables
const searchButton = document.querySelector(`#searchButton`);
const restaurantNameSearch = document.querySelector(`#restaurantSearch`);
const cuisineSearch = document.querySelector(`#cuisine-dropdown`);
const costSearch = document.querySelector(`#cost-dropdown`);
const occasionSearch = document.querySelector(`#occasion-dropdown`);
const SEARCH_API_ENDPOINT = "http://127.0.0.1:5000/search?";
const RESTAURANT_INFO_API_ENDPOINT = "http://127.0.0.1:5000/restaurantinfo?";
const REVIEWS_API_ENDPOINT = "http://127.0.0.1:5000/getreviews?";
const ADDREVIEW_API_ENDPOINT = "http://127.0.0.1:5000/addreview"; 
const loader = document.querySelector(`.loader`);
let addRestaurantButton; 
const searchForm = document.querySelector(`.search-form`);
const searchResultsPane = document.querySelector(`.results`);
const restaurantHeading = document.querySelector('#restaurantNameHeading');
const reviewContainer = document.querySelector(`.reviews`);
const scoresSection = document.querySelector(`.restaurant-scores`);
const summaryContent = document.querySelector(`#summary-content`);
const reviewRestaurantButton = document.querySelector(`#reviewThisRestaurantButton`);
const reviewModal = document.querySelector(`#review-modal`);
const reviewModalClose = document.querySelector(`#close-reviewmodal`);
const consentCheckbox = document.querySelector(`#consent-checkbox`);
const reviewFlashMessage = document.querySelector(`#review-flash-message`);
const restaurantFlashMessage = document.querySelector(`#restaurant-flash-message`);
let previews;

//   Review Modal Variables
const occasionsDropdown = document.querySelector(`#occasions-dropdown`);
const expenseDropdown = document.querySelector(`#expense-dropdown`);
const foodQualityDropdown = document.querySelector(`#foodQuality-dropdown`);
const ambianceDropdown = document.querySelector(`#ambiance-dropdown`);
const customerServiceDropdown = document.querySelector(`#customerService-dropdown`);
const cleanlinessDropdown = document.querySelector(`#cleanliness-dropdown`);
const speedOfServiceDropDown = document.querySelector(`#speedofservice-dropdown`);
const valueForMoneyDropdown = document.querySelector(`#valueForMoney-dropdown`);
const allergyDropdown = document.querySelector(`#allergy-dropdown`);
const overallRatingDropdown = document.querySelector(`#overallRating-dropdown`);
const reviewCommentsText = document.querySelector(`#reviewComments`);
const reviewSubmitButton = document.querySelector(`#reviewSubmitButton`);
const errorSubmissionText = document.querySelector(`#errorSubmissionText`);
const reviewModalForm = document.querySelector(`#reviewModalForm`);
const reviewModalHeading = document.querySelector(`#reviewModalHeading`);
const inputsection = document.querySelector(`.sectionInputs`);
const wordCount = document.querySelector(`#wordcount`);
const reviewModalInputs = [occasionsDropdown, expenseDropdown, foodQualityDropdown, ambianceDropdown, customerServiceDropdown, cleanlinessDropdown, 
    speedOfServiceDropDown, valueForMoneyDropdown, allergyDropdown, overallRatingDropdown];

// Restaurant Modal Variables
const restaurantModal = document.querySelector(`#restaurant-modal`);
const closeRestaurantModalButton = document.querySelector(`#close-restaurantmodal`);
const restaurantErrorSubmissionText = document.querySelector(`#restaurantErrorSubmissionText`);
const restaurantModalForm = document.querySelector(`#restaurantModalForm`);
const restaurantNameInput = document.querySelector(`#restaurantNameInput`);
const cuisineInputDropdown = document.querySelector(`#cuisineInput-dropdown`);
const serviceInputDropdown = document.querySelector(`#serviceInput-dropdown`);
const diningOptionsInputDropdown = document.querySelector(`#diningOptionsInput-dropdown`);
const restaurantSubmitButton = document.querySelector(`#restaurantSubmitButton`);
const restaurantModalInputs = [cuisineInputDropdown, serviceInputDropdown, diningOptionsInputDropdown];


// Functions
function renderResult(result){
    return `
        <div class="search-result-preview" data-id="${result.id}">    
            <h3>${result.restaurantName}</h3>
            <p>Average rating: ${result.avgOverallRating} / 5</p>
        </div>
    `
}

function renderSearchError(){
    const markup = `
        <div class="search-result-error">    
            <h3>No Matching Restaurants Found</h3>
            <hr>
            <p><em>Click the 'Add a restaurant' button below to add a restaurant to our site...</em></p>
            <button type="button" id="addRestaurantButton">Add a restaurant</button>
        </div>
        `;
    searchResultsPane.insertAdjacentHTML(`afterbegin`, markup);
    addRestaurantButton = document.querySelector(`#addRestaurantButton`)
    addRestaurantButton.addEventListener(`click`, showRestaurantModal);
}

function renderSearchAdd() {
    const markup = `
        <div class="search-result-search">
            <h4>Not the restaurant you wanted?</h4>
            <p><em>Click the 'Add a restaurant' button below to add a restaurant to our site...</em></p>
            <button type="button" id="addRestaurantButton">Add a restaurant</button>
        </div>
        `;
    searchResultsPane.insertAdjacentHTML(`beforeend`, markup);
    addRestaurantButton = document.querySelector(`#addRestaurantButton`)
    addRestaurantButton.addEventListener(`click`, showRestaurantModal);
}

function renderAllSearchResults(data) {
    searchResultsPane.innerHTML =  "";
    const markup = data.map(renderResult).join('');
    searchResultsPane.insertAdjacentHTML(`afterbegin`, markup);
    previews = document.querySelectorAll(`.search-result-preview`);
    previews.forEach(item => {
        item.addEventListener(`click`, clickPreview);
    })
    renderSearchAdd();
}

function clickPreview(evt) {
    const parentEle = evt.target.closest(`.search-result-preview`)
    displayRestaurant(parentEle.dataset.id);
}

async function searchRestaurants() {
    // 1. Clear any current results and show loader graphic
    summaryContent.hidden=true
    searchResultsPane.innerHTML =  "";
    loader.hidden = false;
    // 2. Create API Query String dynamically from available search query criteria
    let API_URL = SEARCH_API_ENDPOINT;
    if (restaurantNameSearch.value) {API_URL += `&name=${restaurantNameSearch.value}`}
    if(cuisineSearch.value) {API_URL += `&cuisine=${cuisineSearch.value}`}
    if(costSearch.value) {API_URL += `&cost=${costSearch.value}`}
    if (occasionSearch.value) {API_URL += `&occasion=${occasionSearch.value}`}
    // 3. Send API request to search for restaurants
    const response = await fetch(API_URL)
    const data = await response.json();
    // 4. Render search results to page
    if (data["results"][0]) {
        renderAllSearchResults(data["results"]);
    } else {
        // No results found
        renderSearchError();
    }
    // 5. Hide loader image and reset search form
    searchForm.reset();
    loader.hidden = true;
}

function renderComment(review) {
    return `
        <div class="comment-box">
            <p><i class="fas fa-quote-left"></i>  ${review.comments}  <i class="fas fa-quote-right"></i></p>
        </div>
    `
}

function renderComments(reviews) {
    reviewContainer.innerHTML = ""
    const markup = reviews.map(renderComment).join('');
    reviewContainer.insertAdjacentHTML(`afterbegin`, markup);
}

function convertScores(score) {
    if (score === 1) {return "Terrible"}
    else if (score === 2) {return "Poor"}
    else if (score === 3) {return "Average"}
    else if (score === 4) {return "Very good"}
    else if (score === 5) {return "Excellent"}
    else if (score === 0) {return "No reviews yet"}
}

function renderScores(data) {
    scoresSection.innerHTML = "";
    const markup = `
        <h3>Restaurant Information</h3>    
        <div class="rating-metric">
            <span class="info-description">Open for: </span>
            <span class="info-info">${data.diningOptions}</span>
        </div>
        <div class="rating-metric">
            <span class="info-description">Cuisine served: </span>
            <span class="info-info">${data.cuisineType}</span>
        </div>
        <div class="rating-metric">
            <span class="info-description">Service: </span>
            <span class="info-info">${data.serviceType}</span>
        </div>
        <h3>Average Scores</h3>
        <div class="rating-metric">
            <span class="info-description">Cost per person: </span>
            <span class="info-info">${data.avgExpense} / 5 (${convertScores(data.avgExpense)})</span>
        </div>
        <div class="rating-metric">
            <span class="info-description">Food quality: </span>
            <span class="info-info">${data.avgFoodQuality} / 5 (${convertScores(data.avgFoodQuality)})</span>
        </div>
        <div class="rating-metric">
            <span class="info-description">Ambiance / Atmosphere: </span>
            <span class="info-info">${data.avgAmbiance} / 5 (${convertScores(data.avgAmbiance)})</span>
        </div>
        <div class="rating-metric">
            <span class="info-description">Customer service: </span>
            <span class="info-info">${data.avgServiceQuality} / 5 (${convertScores(data.avgServiceQuality)})</span>
        </div>
        <div class="rating-metric">
            <span class="info-description">Cleanliness: </span>
            <span class="info-info">${data.avgCleanliness} / 5 (${convertScores(data.avgCleanliness)})</span>
        </div>
        <div class="rating-metric">
            <span class="info-description">Speed of service: </span>
            <span class="info-info">${data.avgSpeedOfService} / 5 (${convertScores(data.avgSpeedOfService)})</span>
        </div>
        <div class="rating-metric">
            <span class="info-description">Value for money: </span>
            <span class="info-info">${data.avgValueForMoney} / 5 (${convertScores(data.avgValueForMoney)})</span>
        </div>
        <div class="rating-metric">
            <span class="info-description">Allergy information: </span>
            <span class="info-info">${data.avgAllergyInfoQuality} / 5 (${convertScores(data.avgAllergyInfoQuality)})</span>
        </div>
        <div class="rating-metric">
            <span class="info-description">Overall rating: </span>
            <span class="info-info">${data.avgOverallRating} / 5 (${convertScores(data.avgOverallRating)})</span>
        </div>
    `;
    scoresSection.insertAdjacentHTML(`afterbegin`, markup);
}

function renderRestaurant(data) {
    restaurantHeading.innerText = data.restaurantName;
    reviewThisRestaurantButton.setAttribute('data-id', data.id);
    reviewThisRestaurantButton.setAttribute('data-name', data.restaurantName);
    renderScores(data);
}

async function displayRestaurant(id){
    // Render restaurant to page
    // 1. Send API to get restaurant detailed info
    const response = await fetch(`${RESTAURANT_INFO_API_ENDPOINT}id=${id}`);
    const restaurant = await response.json();
    // 2. Send API to get restaurant comment data
    const reviewResponse = await fetch(`${REVIEWS_API_ENDPOINT}id=${id}`);
    const reviewData = await reviewResponse.json();
    // 3. Render restaurant info, scores and comments
    renderRestaurant(restaurant["results"][0]);
    renderComments(reviewData["results"]);
    summaryContent.hidden=false
};

function showReviewModal(evt) {
    // Show modal, pass active restaurant ID to Modal button and reset modal form fields
    reviewSubmitButton.setAttribute(`data-id`, evt.target.dataset.id)
    reviewModalHeading.innerText = `Review ${evt.target.dataset.name}`
    reviewModalForm.reset();
    reviewSubmitButton.setAttribute("hidden", true)
    reviewModal.classList.add(`show-modal`);
    inputsection.scrollTo(0,0);
    occasionsDropdown.focus()
    errorSubmissionText.hidden=true;
    reviewModalInputs.forEach(function(element) {
        element.classList.remove("highlight-error");
    })
    reviewCommentsText.classList.remove("highlight-error");
}

function closeReviewModal() {
    reviewModal.classList.remove(`show-modal`);
}

function highlightMissingInfo(element) {
    // Apply red highlighting to element if no answer input
    element.classList.add("highlight-error")
}

function validateReviewModalData(evt){
    // Validates review data. Only submits review if all data provided.
    // 1. Remove any prior error formatting from fields
    errorSubmissionText.setAttribute('hidden', true);
    reviewModalInputs.forEach(function(element) {
        element.classList.remove("highlight-error");
    })
    reviewCommentsText.classList.remove("highlight-error");
    // 2. Validate fields and apply highlighting to fields without answers.
    let errorList = 0;
    reviewModalInputs.forEach(function(element) {
        if (!element.options[element.selectedIndex].value) {
            errorList ++;
            highlightMissingInfo(element);
        }
    })
    if (checkLength(reviewCommentsText.value) > 100) {
        errorList ++;
        highlightMissingInfo(reviewCommentsText);
    }
    if (!reviewCommentsText.value) {
        errorList ++;
        highlightMissingInfo(reviewCommentsText);
    }
    // 3. If no errors, then submit review
    if (errorList === 0) {
        addReview(evt.target.dataset.id);
    } else {
        errorSubmissionText.removeAttribute('hidden');
    }
}

async function addReview(id) {
    // Sends review to back-end via POST request
    // 1. Create POST request payload
    const payload = {
        restaurantID: id,
        bestSuitedFor: occasionsDropdown.value,
        expensePerHead: expenseDropdown.value,
        foodQuality: foodQualityDropdown.value,
        ambiance: ambianceDropdown.value,
        serviceQuality: customerServiceDropdown.value,
        cleanliness: cleanlinessDropdown.value,
        speedOfService: speedOfServiceDropDown.value,
        valueForMoney: valueForMoneyDropdown.value,
        allergyInfoProvided: allergyDropdown.value,
        overallRating: overallRatingDropdown.value,
        comments: reviewCommentsText.value,
    };
    // 2. Send POST request
    try {
        const rawResponse = await fetch(ADDREVIEW_API_ENDPOINT, {
            method: "POST",
            body: JSON.stringify(payload),
            mode: "no-cors",
            headers: {
                "Content-Type": "application/json; charset=UTF-8"            },
        });
        // 3. Close modal, show flash message briefly and refresh page with new review details
        displayRestaurant(id);
        closeReviewModal();
        reviewFlashMessage.hidden=false
        setTimeout(function() {reviewFlashMessage.hidden=true;}, 2000);
    } catch(err) {
        // 4. Show browser-level alert if problem with API request
        alert("We had a problem saving your review. Please try again!")
    }
}

function enableReviewSubmission() {
    // Enables the submit review button if checkbox ticked
    if (consentCheckbox.checked === true) {
        reviewSubmitButton.removeAttribute("hidden")
    } else {
        reviewSubmitButton.setAttribute("hidden", true)
    }
}

function checkLength(element) {
    // Returns number of words in data
    return (element.split(" ").length -1);
}

function checkCommentLength() {
    // Provides visual feedback if the user goes over 100 words
    const spaceCount = checkLength(reviewCommentsText.value)
    wordCount.innerText = `${spaceCount} / 100 words`;
    if (spaceCount > 100) {
        wordCount.classList.add("red-text")
    } else {
        wordCount.classList.remove("red-text")
    }
}

function showRestaurantModal(evt) {
    // Show restaurant modal and reset modal form elements
    restaurantModalForm.reset();
    restaurantModal.classList.add(`show-modal`);
    restaurantNameInput.focus();
    restaurantErrorSubmissionText.hidden=true;
    restaurantNameInput.classList.remove("highlight-error");
    restaurantModalInputs.forEach(function(element) {
         element.classList.remove("highlight-error");
     })
}

function closeRestaurantModal() {
    restaurantModal.classList.remove(`show-modal`);
}

function convertToTitleCase(string) {
    // Remove white spaces from beginning / end of string and place in Title Case so all restaurant names are consistent.
    let str = string.toLowerCase();
    str = str.trim();
    str = str.split(" ");
    return str.map(word => {
        return word[0].toUpperCase() + word.slice(1);
    }).join(" ");
}


async function searchNewRestaurant(restaurantName) {
    // Shorter version of the search restaurant function, to be used after adding new restaurant when only name is known
    // 1. Clear results and show loader image
    summaryContent.hidden=true
    searchResultsPane.innerHTML =  "";
    loader.hidden = false;
    // 2. Send API request
    const response = await fetch(`${SEARCH_API_ENDPOINT}&name=${restaurantName}`)
    const data = await response.json();
    // 3. Render results to page
    if (data["results"][0]) {
        renderAllSearchResults(data["results"]);
    } else {
        renderSearchError();
    }
    // 4. Hide loader image and render restaurant to main summary page
    loader.hidden = true;
    displayRestaurant(data["results"][0]["id"]);
}


async function addRestaurant() {
    // 1. Get a converted restaurant name to ensure consistency in the data
    const updatedRestaurantName = convertToTitleCase(restaurantNameInput.value);
    // 2. Create payload for the POST request
    const payload = {
        restaurantName: updatedRestaurantName,
        cuisine: cuisineInputDropdown.value,
        service: serviceInputDropdown.value,
        diningOptions: diningOptionsInputDropdown.value,
    };
    // 3. Send POST request to back end to add restaurant
    try {
        const response = await fetch(RESTAURANT_INFO_API_ENDPOINT, {
            method: "POST",
            body: JSON.stringify(payload),
            mode: "no-cors",
            headers: {
                "Content-Type": "application/json; charset=UTF-8"            },
        });
        // 4. Close modal, show flash message and refresh page to show new restaurant in search results        
        closeRestaurantModal();
        searchNewRestaurant(updatedRestaurantName)
        restaurantFlashMessage.hidden=false
        setTimeout(function() {restaurantFlashMessage.hidden=true;}, 2000);
    } catch(err) {
        // 5. Display a browser-level error if any problems occur
        alert("We had a problem adding this restaurant. Please try again!")
    }
}

function validateRestaurantModalData(evt){
    // 1. Remove any prior error formatting from fields
    restaurantErrorSubmissionText.setAttribute('hidden', true);
    restaurantModalInputs.forEach(function(element) {
        element.classList.remove("highlight-error");
    })
    restaurantNameInput.classList.remove("highlight-error");
    // 2. Validate fields and apply highlighting to fields without valid answers.
    let errorList = 0;
    restaurantModalInputs.forEach(function(element) {
        if (!element.options[element.selectedIndex].value) {
            errorList ++;
            highlightMissingInfo(element);
        }
    })
    if (!restaurantNameInput.value) {
        errorList ++;
        highlightMissingInfo(restaurantNameInput);
    }
    // 3. If no errors, run the add restaurant function.
    if (errorList === 0) {
        addRestaurant();
    } else {
        restaurantErrorSubmissionText.removeAttribute('hidden');
    }
}

// Event Listeners
searchButton.addEventListener(`click`, searchRestaurants)
reviewRestaurantButton.addEventListener(`click`, showReviewModal);
reviewModalClose.addEventListener(`click`, closeReviewModal);
consentCheckbox.addEventListener(`click`, enableReviewSubmission);
reviewSubmitButton.addEventListener(`click`, validateReviewModalData);
reviewCommentsText.addEventListener(`keyup`, checkCommentLength);
closeRestaurantModalButton.addEventListener(`click`, closeRestaurantModal);
restaurantSubmitButton.addEventListener(`click`, validateRestaurantModalData)
restaurantNameSearch.addEventListener(`keydown`, function(evt) {
    if(evt.keyCode == 13) {
        evt.preventDefault();
        searchRestaurants();
    }
})
window.addEventListener(`click`, (evt) => {
    if (evt.target === reviewModal) {
        closeReviewModal();
    }
    else if (evt.target === restaurantModal) {
        closeRestaurantModal();
    }
})
// Startup Actions

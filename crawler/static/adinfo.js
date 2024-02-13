// Initialize a global array to store the previous ad IDs
let previousAds = [];

// Retrieve CSRF token from a cookie
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Get the current ad ID from the URL
const getCurrentAdId = () => {
  const url = window.location.href;
  const adId = url.split('/').pop();
  return adId;
};

// Function to fetch all ads from the database
const fetchAdsFromDatabase = () => {
  return fetch('http://3.104.27.245/v1/scraper')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(jsonData => {
      console.log('API response data:', jsonData.data); // Log the actual data array
      if (!Array.isArray(jsonData.data)) {
        console.error('Invalid response format. Expected an array.');
        return [];
      }
      return jsonData.data.map(ad => ad.ad_id);
    })
    .catch(error => {
      console.error('Failed to fetch ads:', error);
      return [];
    });
};

// Function to shuffle an array randomly
const shuffleArray = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
};

// Navigate to the next random ad
const navigateToNextRandomAd = async () => {
  const currentAdId = parseInt(getCurrentAdId());

  // Retrieve the previousAds array from session storage or create an empty array if it doesn't exist
  previousAds = JSON.parse(sessionStorage.getItem('previousAds')) || [];

  // Store the previous ad ID
  previousAds.push(currentAdId);

  const allAds = await fetchAdsFromDatabase();

  if (allAds.length === 0) {
    console.error('No ads found in the database.');
    return;
  }

  // Shuffle the ads array
  const shuffledAds = shuffleArray(allAds);

  // Find the index of the current ad ID in the shuffled array
  const currentIndex = shuffledAds.indexOf(currentAdId);

  // Get the next ad ID from the shuffled array (cyclically)
  const nextIndex = (currentIndex + 1) % shuffledAds.length;
  const nextAdId = shuffledAds[nextIndex];

  const nextAdUrl = `http://3.104.27.245/crawler/${nextAdId}`;
  window.location.href = nextAdUrl;

  // Save the updated previousAds array to session storage
  sessionStorage.setItem('previousAds', JSON.stringify(previousAds));
};

// Navigate to the previous ad
const navigateToPreviousAd = () => {
  // Retrieve the previousAds array from session storage or create an empty array if it doesn't exist
  previousAds = JSON.parse(sessionStorage.getItem('previousAds')) || [];

  if (previousAds.length > 0) {
    const previousAdId = previousAds.pop(); // Get the last stored previous ad ID
    const previousAdUrl = `http://3.104.27.245/crawler/${previousAdId}`;
    window.location.href = previousAdUrl;

    // Save the updated previousAds array to session storage
    sessionStorage.setItem('previousAds', JSON.stringify(previousAds));
  } else {
    console.log('No previous ads to navigate to.');
  }
};

// Add event listener to the "Next Ad" button to navigate to the next random ad
const nextAdButton = document.getElementById('nextAdButton');
nextAdButton.addEventListener('click', navigateToNextRandomAd);

// Add event listener to the "Previous Ad" button to navigate to the previous ad
const previousAdButton = document.getElementById('previousAdButton');
previousAdButton.addEventListener('click', navigateToPreviousAd);

// Function to handle form submission
function handleSubmit(event) {
  event.preventDefault(); // Prevent the default form submission

  const adId = getCurrentAdId();
  const noteInput = document.getElementById('noteInput').value;
  const url = `http://3.104.27.245/v1/crawler/update_ad/${adId}`;
  const csrfToken = getCookie('csrfmiddlewaretoken');

  // Create a new XMLHttpRequest object
  const xhr = new XMLHttpRequest();
  xhr.open('PUT', url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.setRequestHeader('X-CSRFToken', csrfToken);

  // Set up a callback function to handle the request response
  xhr.onload = function () {
    if (xhr.status === 200) {
      // Request successful, display the note or update the page as needed
      console.log('Note saved successfully');
    } else {
      // Request failed, handle the error appropriately
      console.error('Failed to save note:', xhr.status);
    }
  };

  // Create a JSON payload with the note data
  const payload = JSON.stringify({ notes: noteInput });

  // Send the PUT request
  xhr.send(payload);
}

// Attach the form submission handler
const form = document.getElementById('notesForm');
form.addEventListener('submit', handleSubmit);
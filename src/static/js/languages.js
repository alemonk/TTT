// Define translations for each text element
const translations = {
  'en': {
    'homePage': 'Home page',
    'notes': 'Notes',
    'quickTest': 'Quick Test',
    'customTest': 'Custom Test',
    'history': 'History',
    'settings': 'Settings',
    'logout': 'Logout',
    'login': 'Login',
    'signUp': 'Sign up'
  },
  'it': {
    'homePage': 'Pagina principale',
    'notes': 'Note',
    'quickTest': 'Test rapido',
    'customTest': 'Test personalizzato',
    'history': 'Cronologia',
    'settings': 'Impostazioni',
    'logout': 'Disconnetti',
    'login': 'Accedi',
    'signUp': 'Iscriviti'
  }
};

$(document).ready(function() {
  // Load language preference from the database using a fetch request
  fetch('/language')
  .then(response => response.json())
  .then(data => {
    // Check if a language preference was returned
    if (data.language) {
      // Update interface based on language preference
      updateInterface(data.language);
    }
  });
});

// Save language preference to local storage
function saveLanguagePreference(lang) {
  localStorage.setItem('language', lang);
}

// Load language preference from local storage
function loadLanguagePreference() {
  return localStorage.getItem('language');
}

// Update interface based on language preference
function updateInterface(lang) {
    // Update the text of the button element
    document.querySelector('#dropdownMenuButton').textContent = lang.toUpperCase();

    // Update screen elements
    document.querySelector('#index').textContent = translations[lang]['homePage'];
    document.querySelector('#notes').textContent = translations[lang]['notes'];
    document.querySelector('#quick_test').textContent = translations[lang]['quickTest'];
    document.querySelector('#custom_test').textContent = translations[lang]['customTest'];
    document.querySelector('#history').textContent = translations[lang]['history'];
    document.querySelector('#settings').textContent = translations[lang]['settings'];
    document.querySelector('#logout').textContent = translations[lang]['logout'];
    // document.querySelector('#login').textContent = translations[lang]['login'];
    // document.querySelector('#signUp').textContent = translations[lang]['signUp'];

    // Update text content of elements when user selects a different language
    document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', event => {
        // Get the selected language from the clicked element
        const lang = event.target.textContent === 'English' ? 'en' : 'it';

        // Save language preference to local storage
        saveLanguagePreference(lang);

        // Update interface based on language preference
        updateInterface(lang);
    });
    });
}

function onClickLanguage(lang) {
  // Save language preference to local storage
  saveLanguagePreference(lang);

  // Call the Python function to modify the database
  fetch('/language', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ language: lang })
  })
  .then(response => response.json())
  .then(data => {
    // Check if the operation was successful
    if (data.success) {
      // Update interface based on language preference
      updateInterface(lang);
    } else {
      // Handle error
      console.error('An error occurred while changing language');
    }
  });
}

// Load language preference from local storage and update interface on page load
const lang = loadLanguagePreference();
if (lang) {
  updateInterface(lang);
}

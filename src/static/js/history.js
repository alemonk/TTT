function deleteTest(testId) {
  fetch('/delete-test', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ testId })
  }).then(response => response.json())
    .then(data => {
      if (data.success) {
        location.reload();
      }
    });
}


function toggleAnswersAndGuesses() {
    // Get all the answer and guess cells in the table
    const answerCells = document.querySelectorAll('td:nth-child(2)');
    const guessCells = document.querySelectorAll('td:nth-child(3)');
    // Loop through the answer and guess cells
    for (let i = 0; i < answerCells.length; i++) {
        // Toggle the visibility of the answer and guess cells
        if (answerCells[i].style.display === 'none') {
            answerCells[i].style.display = 'table-cell';
            guessCells[i].style.display = 'table-cell';
        } else {
            answerCells[i].style.display = 'none';
            guessCells[i].style.display = 'none';
        }
    }
}


function showTest(element, testId) {
  // Get all the test data elements
  const testDataElements = document.querySelectorAll('.test-data');
  // Loop through the test data elements
  for (let i = 0; i < testDataElements.length; i++) {
    // Check if the current test data element is not the one that was clicked
    if (testDataElements[i].id !== `test-data-${testId}`) {
      // Hide and clear the test data element
      testDataElements[i].style.display = 'none';
      testDataElements[i].innerHTML = '';
    }
  }

  // Get the element where the test data will be displayed
  const testData = document.querySelector(`#test-data-${testId}`);
  // If the test data is hidden, fetch it from the server and display it
  if (testData.style.display === 'none') {
    // Create a form data object with the test ID
    const formData = new FormData();
    formData.append('test_id', testId);
    // Fetch the test data from the Python route
    fetch('/get-test', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        // Check if there is an error in the response
        if (data.error) {
          // Display the error message
          testData.textContent = data.error;
        } else {
          // Create a table element to display the test data
          const table = document.createElement('table');
          table.classList.add('table');

          // Create a table header row with three columns
          const headerRow = document.createElement('tr');
          const questionHeader = document.createElement('th');
          questionHeader.textContent = 'Question';
          const answerHeader = document.createElement('th');
          answerHeader.textContent = 'Answer';
          const guessHeader = document.createElement('th');
          guessHeader.textContent = 'Your guess';
          headerRow.appendChild(questionHeader);
          headerRow.appendChild(answerHeader);
          headerRow.appendChild(guessHeader);
          table.appendChild(headerRow);

          // Loop through the questions, answers, and guesses in the response data
          for (let i = 0; i < data.questions.length; i++) {
            // Create a table row for each question, answer, and guess triplet
            const row = document.createElement('tr');
            const questionCell = document.createElement('td');
            questionCell.textContent = data.questions[i];
            const answerCell = document.createElement('td');
            answerCell.textContent = data.answers[i];
            const guessCell = document.createElement('td');
            guessCell.textContent = data.guesses[i];
            row.appendChild(questionCell);
            row.appendChild(answerCell);
            row.appendChild(guessCell);

            // Append the row to the table element
            table.appendChild(row);
          }

          // Append the table to the test data element
          testData.appendChild(table);

          // Hide the answers and guesses by default
          toggleAnswersAndGuesses();
        }
        // Show the test data element
        testData.style.display = 'block';
      });
  } else {
    // Hide and clear the test data element
    testData.style.display = 'none';
    testData.innerHTML = '';
  }
}

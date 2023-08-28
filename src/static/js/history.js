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


function showTest(element, testId) {
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

          // Create a table header row with two columns
          const headerRow = document.createElement('tr');
          const questionHeader = document.createElement('th');
          questionHeader.textContent = 'Question';
          const answerHeader = document.createElement('th');
          answerHeader.textContent = 'Answer';
          headerRow.appendChild(questionHeader);
          headerRow.appendChild(answerHeader);
          table.appendChild(headerRow);

          // Loop through the questions and answers in the response data
          for (let i = 0; i < data.questions.length; i++) {
            // Create a table row for each question and answer pair
            const row = document.createElement('tr');
            const questionCell = document.createElement('td');
            questionCell.textContent = data.questions[i];
            const answerCell = document.createElement('td');
            answerCell.textContent = data.answers[i];
            row.appendChild(questionCell);
            row.appendChild(answerCell);

            // Append the row to the table element
            table.appendChild(row);
          }

          // Append the table to the test data element
          testData.appendChild(table);
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

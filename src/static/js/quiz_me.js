// Store the value of answer
var answer;

// Clear the content of the output and answer-buttons div elements
function clearOutput() {
    document.getElementById('output').textContent = '';
    document.getElementById('answer-buttons').innerHTML = '';
    document.getElementById('answer-output').textContent = '';
}

// Create answer buttons and append them to the answer-buttons div element
function createAnswerButtons(answers) {
    var answerButtonsDiv = document.getElementById('answer-buttons');
    for (var i = 0; i < answers.length; i++) {
        var answerButton = document.createElement('button');
        answerButton.type = 'button';
        answerButton.className = 'btn btn-primary';
        answerButton.style.marginRight = '5px';
        answerButton.textContent = answers[i].label;
        answerButton.style.backgroundColor = answers[i].color;
        answerButtonsDiv.appendChild(answerButton);
    }
}

// Add an event listener to the open-question-button element
document.getElementById('open-question-button').addEventListener('click', function() {
    clearOutput();

    fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({type_of_question: 'open question'})
    })
        .then(response => response.json())
        .then(data => {
            var outputDiv = document.getElementById('output');
            // Remove this line to avoid duplicating the question
            // outputDiv.textContent = data.question;
            answer = data.answer;

            // Create a container div element for the question, textarea, submit button, and answer-output
            var containerDiv = document.createElement('div');
            containerDiv.style.display = 'block';
            containerDiv.className = 'p-5 bg-primary-subtle rounded-5'; // Add the desired class here
            outputDiv.appendChild(containerDiv);

            // Create a div element for the question
            var questionDiv = document.createElement('div');
            questionDiv.textContent = data.question;
            containerDiv.appendChild(questionDiv);

            // Create a textarea element for user input
            var textarea = document.createElement('textarea');
            textarea.style.width = '100%';
            textarea.style.boxSizing = 'border-box';
            textarea.rows = 4;
            containerDiv.appendChild(textarea);

            // Create a submit button for user input
            var submitButton = document.createElement('button');
            submitButton.type = 'button';
            submitButton.className = 'btn btn-primary';
            submitButton.style.marginTop = '10px';
            submitButton.textContent = 'Submit';
            containerDiv.appendChild(submitButton);

            // Create a div element for the answer-output
            var answerOutputDiv = document.createElement('div');
            containerDiv.appendChild(answerOutputDiv);

            // Add an event listener to the submit button
            submitButton.addEventListener('click', function() {
                var guess = textarea.value;
                var question = data.question;
                fetch('/open_question_check_answer', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ guess: guess, question: question, answer: answer })
                })
                    .then(response => response.json())
                    .then(data => {
                        answerOutputDiv.textContent = data.response;
                    });
            });
        });
});

// Add an event listener to the true-false-button element
document.getElementById('true-false-button').addEventListener('click', function() {
    clearOutput();

    fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({type_of_question: 'true or false'})
    })
        .then(response => response.json())
        .then(data => {
            var outputDiv = document.getElementById('output');
            // Remove this line to avoid duplicating the question
            // outputDiv.textContent = data.question;
            answer = data.answer;

             // Create a container div element for the question, textarea, submit button, and answer-output
             var containerDiv = document.createElement('div');
             containerDiv.style.display = 'block';
             containerDiv.className = 'p-5 bg-primary-subtle rounded-5'; // Add the desired class here
             outputDiv.appendChild(containerDiv);

             // Create a div element for the question
             var questionDiv = document.createElement('div');
             questionDiv.textContent = data.question;
             containerDiv.appendChild(questionDiv);

             // Create a div element for the answer-buttons
             var answerButtonsDiv = document.createElement('div');
             containerDiv.appendChild(answerButtonsDiv);

             // Create a div element for the answer-output
             var answerOutputDiv = document.createElement('div');
             containerDiv.appendChild(answerOutputDiv);

             // Create answer buttons and append them to the answer-buttons div element
             var answers = [
                 { label: 'True', color: '#29A6FF' },
                 { label: 'False', color: '#29A6FF' }
             ];
             for (var i = 0; i < answers.length; i++) {
                 var answerButton = document.createElement('button');
                 answerButton.type = 'button';
                 answerButton.className = 'btn btn-primary my-2';
                 answerButton.style.marginRight = '5px';
                 answerButton.textContent = answers[i].label;
                 answerButton.style.backgroundColor = answers[i].color;
                 answerButtonsDiv.appendChild(answerButton);
             }

            // Add an event listener to the answer buttons
            var answerButtons = answerButtonsDiv.querySelectorAll('button'); // Fix this line to correctly select the answer buttons
            for (var i = 0; i < answerButtons.length; i++) {
                answerButtons[i].addEventListener('click', function() {
                    var guess = this.textContent;
                    var question = data.question;
                    fetch('/true_or_false_check_answer', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ guess: guess, question: question, answer: answer })
                    })
                        .then(response => response.json())
                        .then(data => {
                            answerOutputDiv.textContent = data.response;
                            if (data.response.startsWith("Correct")) {
                                this.style.backgroundColor = '#28a745';
                            } else {
                                this.style.backgroundColor = '#dc3545';
                            }
                        });
                });
            }
        });
});

// Add an event listener to the closed-question-button element
document.getElementById('closed-question-button').addEventListener('click', function() {
    clearOutput();

    fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({type_of_question: 'closed question'})
    })
        .then(response => response.json())
        .then(data => {
            var outputDiv = document.getElementById('output');
            // Remove this line to avoid duplicating the question
            // outputDiv.textContent = data.question;
            answer = data.answer;

             // Create a container div element for the question, textarea, submit button, and answer-output
             var containerDiv = document.createElement('div');
             containerDiv.style.display = 'block';
             containerDiv.className = 'p-5 bg-primary-subtle rounded-5'; // Add the desired class here
             outputDiv.appendChild(containerDiv);

             // Create a div element for the question
             var questionDiv = document.createElement('div');
             questionDiv.textContent = data.question;
             containerDiv.appendChild(questionDiv);

             // Create a div element for the answer-buttons
             var answerButtonsDiv = document.createElement('div');
             containerDiv.appendChild(answerButtonsDiv);

             // Create a div element for the answer-output
             var answerOutputDiv = document.createElement('div');
             containerDiv.appendChild(answerOutputDiv);

             // Create answer buttons and append them to the answer-buttons div element
             var answers = [
                 { label: 'A', color: '#29A6FF' },
                 { label: 'B', color: '#29A6FF' },
                 { label: 'C', color: '#29A6FF' },
                 { label: 'D', color: '#29A6FF' }
             ];
             for (var i = 0; i < answers.length; i++) {
                 var answerButton = document.createElement('button');
                 answerButton.type = 'button';
                 answerButton.className = 'btn btn-primary my-2';
                 answerButton.style.marginRight = '5px';
                 answerButton.textContent = answers[i].label;
                 answerButton.style.backgroundColor = answers[i].color;
                 answerButtonsDiv.appendChild(answerButton);
             }

            // Add an event listener to the answer buttons
            var answerButtons = answerButtonsDiv.querySelectorAll('button'); // Fix this line to correctly select the answer buttons
            for (var i = 0; i < answerButtons.length; i++) {
                answerButtons[i].addEventListener('click', function() {
                    var guess = this.textContent;
                    var question = data.question;
                    fetch('/closed_question_check_answer', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ guess: guess, question: question, answer: answer })
                    })
                        .then(response => response.json())
                        .then(data => {
                            answerOutputDiv.textContent = data.response;
                            if (data.response.startsWith("Correct")) {
                                this.style.backgroundColor = '#28a745';
                            } else {
                                this.style.backgroundColor = '#dc3545';
                            }
                        });
                });
            }
        });
});

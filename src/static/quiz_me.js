let slider = document.getElementById("difficultySlider");
let output = document.getElementById("difficulty");
output.innerHTML = slider.value == 1 ? "Easy" : (slider.value == 2 ? "Medium" : "Hard");

slider.oninput = function() {
    output.innerHTML = this.value == 1 ? "Easy" : (this.value == 2 ? "Medium" : "Hard");
}

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

    let difficulty = document.getElementById("difficulty").innerHTML;

    fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({difficulty: difficulty, type_of_question: 'open question'})
    })
        .then(response => response.json())
        .then(data => {
            var outputDiv = document.getElementById('output');
            outputDiv.textContent = data.question;
            answer = data.answer;

            // Create a container div element for the textarea and submit button
            var containerDiv = document.createElement('div');
            containerDiv.style.display = 'block';
            outputDiv.appendChild(containerDiv);

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
                        var answerOutputDiv = document.getElementById('answer-output');
                        answerOutputDiv.textContent = data.response;
                    });
            });
        });
});

// Add an event listener to the true-false-button element
document.getElementById('true-false-button').addEventListener('click', function() {
    clearOutput();

    let difficulty = document.getElementById("difficulty").innerHTML;

    fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({difficulty: difficulty, type_of_question: 'true or false'})
    })
        .then(response => response.json())
        .then(data => {
            var outputDiv = document.getElementById('output');
            outputDiv.textContent = data.question;
            answer = data.answer;

            // Create answer buttons
            var answers = [
                { label: 'True', color: '#007bff' },
                { label: 'False', color: '#007bff' }
            ];
            createAnswerButtons(answers);

            // Add an event listener to the answer buttons
            var answerButtons = document.querySelectorAll('#answer-buttons > button');
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
                            var answerOutputDiv = document.getElementById('answer-output');
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

    let difficulty = document.getElementById("difficulty").innerHTML;

    fetch('/question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({difficulty: difficulty, type_of_question: 'closed question'})
    })
        .then(response => response.json())
        .then(data => {
            var outputDiv = document.getElementById('output');
            outputDiv.textContent = data.question;
            answer = data.answer;

            // Create answer buttons
            var answers = [
                { label: 'A', color: '#007bff' },
                { label: 'B', color: '#007bff' },
                { label: 'C', color: '#007bff' },
                { label: 'D', color: '#007bff' }
            ];
            createAnswerButtons(answers);

            // Add an event listener to the answer buttons
            var answerButtons = document.querySelectorAll('#answer-buttons > button');
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
                            var answerOutputDiv = document.getElementById('answer-output');
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

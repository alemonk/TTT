// Clear the content of the output div element
function clearOutput() {
    document.getElementById('output').innerHTML = '';
}

// Add an event listener to the createTestButton element
function createTest() {
    clearOutput();

    // Notes to use
    var selectedNotes = Array.from(document.querySelectorAll('.form-check-input:checked'))
        .map(checkbox => checkbox.nextElementSibling.textContent.trim());

    console.log(selectedNotes);

    let numOpenQuestions = parseInt(document.getElementById("numOpenQuestions").value);
    let numTrueFalseQuestions = parseInt(document.getElementById("numTrueFalseQuestions").value);
    let numClosedQuestions = parseInt(document.getElementById("numClosedQuestions").value);

    let numQuestions = numOpenQuestions + numTrueFalseQuestions + numClosedQuestions;

    let questionTypes = ['open question', 'true or false', 'closed question'];
    let numQuestionTypesPerType = [numOpenQuestions, numTrueFalseQuestions, numClosedQuestions];

    // Create a container div element for the progress bar
    var containerDiv = document.createElement('div');
    containerDiv.style.display = 'block';
    containerDiv.style.width = '90%';
    containerDiv.style.marginLeft = 'auto';
    containerDiv.style.marginRight = 'auto';

    // Create a progress bar element
    var progressBar = document.createElement('div');
    progressBar.className = 'progress bg-primary';
    progressBar.role = 'progressbar';
    progressBar.style.width = '0%';
    progressBar.style.display = 'flex';
    progressBar.style.justifyContent = 'center';
    progressBar.style.alignItems = 'center';

    containerDiv.appendChild(progressBar);

    // Create a progress text element
    var progressText = document.createElement('p');
    progressText.textContent = '0/' + numQuestions;
    containerDiv.appendChild(progressText);

    var outputDiv = document.getElementById('output');
    outputDiv.appendChild(containerDiv);

    let numQuestionsGenerated = 0;

    // Create an array to store the generated questions
    let generated_questions = [];
    // Create an array to store the user guesses
    let user_guesses = [];

    // Create a queue class
    class Queue {
        constructor() {
            this.items = [];
        }

        // Add an item to the queue
        enqueue(item) {
            this.items.push(item);
        }

        // Remove an item from the queue
        dequeue() {
            if (this.isEmpty()) {
                return null;
            }
            return this.items.shift();
        }

        // Check if the queue is empty
        isEmpty() {
            return this.items.length == 0;
        }
    }

    // Create a global queue instance
    var queue = new Queue();

    const controller = new AbortController();
    const signal = controller.signal;
    createCancelButton(controller);

    // Create a function to process the queue
    function processQueue() {
        // Check if the queue is empty
        if (queue.isEmpty()) {
            return;
        }

        // Get the first item from the queue
        var item = queue.dequeue();

        // Process the next item in the queue
        // BE CAREFUL, IT SENDS ALL THE REQUESTS AT THE SAME TIME
        // Comment 'processQueue2' before uncommenting this one, and vice versa
        // This is 'processQueue1'
        // processQueue();

        // Send a request to the /question endpoint with the item data
        fetch('/question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            signal,
            body: JSON.stringify({ type_of_question: item.type_of_question, selected_notes: selectedNotes })
        })
            .then(response => response.json())
            .then(data => {

                createTestButton.classList.add('disabled')

                // Update the progress bar and text
                numQuestionsGenerated++;
                let progressPercentage = Math.floor((numQuestionsGenerated / numQuestionTypesPerType.reduce((a, b) => parseInt(a) + parseInt(b), 0)) * 100);
                progressBar.style.width = progressPercentage + '%';
                progressText.textContent = numQuestionsGenerated + '/' + (numQuestionTypesPerType.reduce((a, b) => parseInt(a) + parseInt(b), 0));

                // Add the generated question to the generated_questions array
                generated_questions.push(data);

                // Check if all questions have been generated
                if (queue.isEmpty()) {
                    // All questions have been generated, so display them on the page
                    for (let k=0; k < generated_questions.length; k++) {
                        let data=generated_questions[k];

                        // Create a container div element for the question and answer
                        var containerDiv=document.createElement('div');
                        containerDiv.className='card bg-light-subtle rounded-2 m-3 p-3 shadow';
                        outputDiv.appendChild(containerDiv);

                        // Create a p element for the question
                        var questionP=document.createElement('p');
                        questionP.textContent=data.question;
                        containerDiv.appendChild(questionP);

                        if (data.type_of_question == 'open question') {
                            // Create a textarea element for user input
                            let textarea = document.createElement('textarea');
                            textarea.style.width = '100%';
                            textarea.style.boxSizing = 'border-box';
                            textarea.rows = 4;
                            containerDiv.appendChild(textarea);

                            // Create a submit button for user input
                            var submitButton=document.createElement('button');
                            submitButton.type='button';
                            submitButton.className='btn btn-secondary my-2';
                            submitButton.style.marginTop='10px';
                            submitButton.textContent='Save';
                            containerDiv.appendChild(submitButton);

                            // Add an event listener to the submit button
                            submitButton.addEventListener('click', (function(containerDiv) {
                                return function() {
                                    // Change text on the button to show that the answer was correctly saved
                                    this.textContent='Saving the answer...';

                                    var guess = textarea.value;
                                    var question = data.question;
                                    var answer = data.answer;

                                    // Add guess and correct answer to the respective arrays
                                    user_guesses.push({ question: question, guess: guess, answer: answer, type_of_question: data.type_of_question })

                                    fetch('/open_question_check_answer', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json'
                                        },
                                        body: JSON.stringify({ guess: guess, question: question, answer: answer })
                                    })
                                        .then(response => response.json())
                                        .then(data => {
                                            // Change text on the button to show that the answer was correctly saved
                                            this.textContent='Answer saved!';
                                            this.className='btn btn-primary my-2';

                                            var answerP = document.createElement('p');
                                            answerP.className = 'answer card-footer bg-light-subtle';
                                            answerP.textContent = data.response;
                                            answerP.classList.add('visually-hidden');
                                            containerDiv.appendChild(answerP);
                                        });
                                };
                            })(containerDiv));
                        } else if (data.type_of_question == 'true or false') {
                            // Create answer buttons
                            var answers = [
                                { label: 'True' },
                                { label: 'False' }
                            ];
                            createAnswerButtons(answers, containerDiv);

                            // Add an event listener to the answer buttons
                            var answerButtons = containerDiv.querySelectorAll('button');
                            for (var i = 0; i < answerButtons.length; i++) {
                                (function(containerDiv) {
                                    answerButtons[i].addEventListener('click', function() {
                                        var guess = this.textContent;
                                        var question = data.question;

                                        // Add guess and correct answer to the respective arrays
                                        user_guesses.push({ question: data.question, guess: guess, answer: data.answer, type_of_question: data.type_of_question })

                                        fetch('/true_or_false_check_answer', {
                                            method: 'POST',
                                            headers: {
                                                'Content-Type': 'application/json'
                                            },
                                            body: JSON.stringify({ guess: guess, question: question, answer: data.answer })
                                        })
                                            .then(response => response.json())
                                            .then(data => {
                                                // Clear the previous answer
                                                var previousAnswerP = containerDiv.querySelector('.answer');
                                                if (previousAnswerP) {
                                                    previousAnswerP.remove();
                                                }

                                                // Display the new answer
                                                var answerP = document.createElement('p');
                                                answerP.className = 'answer card-footer bg-light-subtle';
                                                answerP.textContent = data.response;
                                                answerP.classList.add('visually-hidden');
                                                containerDiv.appendChild(answerP);

                                                // Remove the 'primary' class from all the answer buttons
                                                var answerButtons = containerDiv.querySelectorAll('button');
                                                for (var j = 0; j < answerButtons.length; j++) {
                                                    answerButtons[j].classList.remove('btn-primary');
                                                    answerButtons[j].classList.add('btn-secondary');
                                                }

                                                // Add the 'primary' class to the clicked button
                                                this.classList.remove('btn-secondary');
                                                this.classList.add('btn-primary');
                                            });
                                    });
                                })(containerDiv);
                            }

                        } else if (data.type_of_question == 'closed question') {
                            // Create answer buttons
                            var answers = [
                                { label: 'A' },
                                { label: 'B' },
                                { label: 'C' },
                                { label: 'D' }
                            ];
                            createAnswerButtons(answers, containerDiv);

                            // Add an event listener to the answer buttons
                            var answerButtons = containerDiv.querySelectorAll('button');
                            for (var i = 0; i < answerButtons.length; i++) {
                                (function(containerDiv) {
                                    answerButtons[i].addEventListener('click', function() {
                                        var guess = this.textContent;
                                        var question = data.question;

                                        // Add guess and correct answer to the respective arrays
                                        user_guesses.push({ question: data.question, guess: guess, answer: data.answer, type_of_question: data.type_of_question })

                                        fetch('/closed_question_check_answer', {
                                            method: 'POST',
                                            headers: {
                                                'Content-Type': 'application/json'
                                            },
                                            body: JSON.stringify({ guess: guess, question: question, answer: data.answer })
                                        })
                                            .then(response => response.json())
                                            .then(data => {
                                                // Clear the previous answer
                                                var previousAnswerP = containerDiv.querySelector('.answer');
                                                if (previousAnswerP) {
                                                    previousAnswerP.remove();
                                                }

                                                // Display the new answer
                                                var answerP = document.createElement('p');
                                                answerP.className = 'answer card-footer bg-light-subtle';
                                                answerP.textContent = data.response;
                                                answerP.classList.add('visually-hidden');
                                                containerDiv.appendChild(answerP);

                                                // Remove the 'primary' class from all the answer buttons
                                                var answerButtons = containerDiv.querySelectorAll('button');
                                                for (var j = 0; j < answerButtons.length; j++) {
                                                    answerButtons[j].classList.remove('btn-primary');
                                                    answerButtons[j].classList.add('btn-secondary');
                                                }

                                                // Add the 'primary' class to the clicked button
                                                this.classList.remove('btn-secondary');
                                                this.classList.add('btn-primary');
                                            });
                                    });
                                })(containerDiv);
                            }
                        }
                    }

                    // Call the createCheckAnswersButton function to create the button
                    createCheckAnswersButton(outputDiv, user_guesses);
                }

                // Process the next item in the queue
                // Comment 'processQueue1' before uncommenting this one, and vice versa
                // This is 'processQueue2'
                processQueue();

            })
            .catch(error => console.error(error));

    }

    // Modify the for loop to enqueue the requests instead of sending them directly
    for (let i = 0; i < questionTypes.length; i++) {
        let type_of_question = questionTypes[i];
        let numQuestionsPerType = numQuestionTypesPerType[i];

        for (let j=0; j < numQuestionTypesPerType[i]; j++) {

            // Print to console for debugging
            console.log('type_of_question: ', type_of_question)

            // Enqueue the request data
            queue.enqueue({ type_of_question: type_of_question });
        }
    }

    // Start processing the queue
    processQueue();
}


// Define a function to create the buttons
function createCheckAnswersButton(outputDiv, user_guesses) {
    // Create a div element to contain the buttons
    let buttonsDiv = document.createElement('div');
    outputDiv.appendChild(buttonsDiv);

    // Create the 'check answers' button
    let checkAnswersButton = document.createElement('button');
    checkAnswersButton.type = 'button';
    checkAnswersButton.className = 'btn btn-secondary m-2';
    checkAnswersButton.textContent = 'Check Answers';
    buttonsDiv.appendChild(checkAnswersButton);

    // In the event listener for the 'check answers' button, remove the visually-hidden class from all the answerP elements
    checkAnswersButton.addEventListener('click', function() {
        // Make the 'check answers' button not clickable anymore
        checkAnswersButton.classList.add('disabled');

        // Show correct answers
        let answerPs = outputDiv.querySelectorAll('p.visually-hidden');
        for (let i = 0; i < answerPs.length; i++) {
            answerPs[i].classList.remove('visually-hidden');
        }

        // Add the disabled attribute to all the answer/submit buttons
        let buttons = outputDiv.querySelectorAll('button');
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].setAttribute('disabled', 'disabled');
        }

        // Call the createSaveTestButton function to create the button
        createSaveTestButton(buttonsDiv, user_guesses);
    });
}

function createSaveTestButton(buttonsDiv, user_guesses) {
    // Create the 'save test' button
    let saveButton = document.createElement('button');
    saveButton.type = 'button';
    saveButton.className = 'btn btn-secondary m-2';
    saveButton.textContent = 'Save test';
    buttonsDiv.appendChild(saveButton);

    // In the event listener for the 'save test' button, call the save_test_in_database function using fetch
    saveButton.addEventListener('click', function() {
        // Call the save_test_in_database function using fetch
        fetch('/save_test_in_database', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user_guesses)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // The test was successfully saved
                saveButton.textContent='Test saved!';
                saveButton.className = 'btn btn-success m-2';
            } else {
                // There was an error while saving the test
                saveButton.textContent='Error! test not saved';
                saveButton.className = 'btn btn-danger m-2';
                console.error(data.error);
            }
            saveButton.classList.add('disabled');
        });
    });
}

function errorMessage() {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show mx-3';
    alert.setAttribute('role', 'alert');

    const text = document.createTextNode('Please add at least one note first.');
    alert.appendChild(text);

    const button = document.createElement('button');
    button.className = 'btn-close';
    button.setAttribute('type', 'button');
    button.setAttribute('data-bs-dismiss', 'alert');
    button.setAttribute('aria-label', 'Close');
    alert.appendChild(button);

    document.body.appendChild(alert);
}

// Create answer buttons and append them to the container div element
function createAnswerButtons(answers, containerDiv) {
    // Create a row element
    var row = document.createElement('div');
    row.className = 'row';
    row.style.width = 'fit-content';
    row.style.marginLeft = 'auto';
    row.style.marginRight = 'auto';

    for (var i = 0; i < answers.length; i++) {
        var answerButton = document.createElement('button');
        answerButton.type = 'button';
        answerButton.className = 'btn btn-secondary my-2';
        answerButton.style.marginRight = '5px';
        answerButton.textContent = answers[i].label;
        answerButton.style.width = 'fit-content';
        answerButton.style.backgroundColor = answers[i].color;
        // Append the answer button to the row element
        row.appendChild(answerButton);
    }
    // Append the row element to the container div
    containerDiv.appendChild(row);
}

// Create the 'cancel' button
function createCancelButton(controller) {
    // Create the 'cancel' button
    let cancelButton = document.createElement('button');
    cancelButton.type = 'button';
    cancelButton.className = 'btn btn-danger m-2';
    cancelButton.textContent = 'Cancel';
    crateTestDiv.appendChild(cancelButton);

    // In the event listener for the 'cancel' button, remove all elements from the queue
    cancelButton.addEventListener('click', function() {
        controller.abort();
    });
}


$(document).ready(function(){
    $('.folder-checkbox').change(function() {
        var folderId = $(this).val();
        if(this.checked) {
            $('.note-in-folder-' + folderId).prop('checked', true);
        } else {
            $('.note-in-folder-' + folderId).prop('checked', false);
        }
    updateCreateTestButton();
    });

    $('.note-checkbox').change(function() {
        var noteId = $(this).val();
        var folderId = $(this).closest('.form-check').prevAll('.form-check').first().find('.folder-checkbox').val();
        if($('.note-in-folder-' + folderId + ':checked').length == $('.note-in-folder-' + folderId).length) {
            $('#folderCheck' + folderId).prop('checked', true);
        } else {
            $('#folderCheck' + folderId).prop('checked', false);
        }
        updateCreateTestButton();
    });

    function updateCreateTestButton() {
        if($('.note-checkbox:checked').length > 0) {
            $('#createTestButton').removeClass('disabled');
        } else {
            $('#createTestButton').addClass('disabled');
        }
    }

    $('#createTestButton').click(function() {
        // Call the createTest function from quick_test.js
        createTest();
    });
});

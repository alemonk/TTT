// Clear the content of the output div element
function clearOutput() {
    document.getElementById('output').innerHTML = '';
}

// Create answer buttons and append them to the container div element
function createAnswerButtons(answers, containerDiv) {
    for (var i = 0; i < answers.length; i++) {
        var answerButton = document.createElement('button');
        answerButton.type = 'button';
        answerButton.className = 'btn btn-secondary my-2';
        answerButton.style.marginRight = '5px';
        answerButton.textContent = answers[i].label;
        answerButton.style.backgroundColor = answers[i].color;
        containerDiv.appendChild(answerButton);
    }
}

// Add an event listener to the createTestButton element
document.getElementById('createTestButton').addEventListener('click', function() {
    clearOutput();

    fetch('/get_preferences', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({type_of_question: 'closed question'})
    })
    .then(response => response.json())
    .then(data => {

        let numOpenQuestions = data.num_open_q;
        let numTrueFalseQuestions = data.num_tf_q;
        let numClosedQuestions = data.num_closed_q;

        let numQuestions = numOpenQuestions + numTrueFalseQuestions + numClosedQuestions;

        let questionTypes = ['open question', 'true or false', 'closed question'];
        let numQuestionTypesPerType = [numOpenQuestions, numTrueFalseQuestions, numClosedQuestions];

        // Create a container div element for the progress bar
        var containerDiv = document.createElement('div');
        containerDiv.style.display = 'block';
        containerDiv.style.width = '100%';

        // Create a progress bar element
        var progressBar = document.createElement('div');
        progressBar.className = 'progress bg-primary';
        progressBar.role = 'progressbar';
        progressBar.style.width = '0%';

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

        // Create a function to process the queue
        function processQueue() {
            // Check if the queue is empty
            if (queue.isEmpty()) {
                return;
            }

            // Get the first item from the queue
            var item = queue.dequeue();

            // Send a request to the /question endpoint with the item data
            fetch('/question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ type_of_question: item.type_of_question })
            })
                .then(response => response.json())
                .then(data => {
                    // Update the progress bar and text
                    numQuestionsGenerated++;
                    let progressPercentage = Math.floor((numQuestionsGenerated / numQuestionTypesPerType.reduce((a, b) => parseInt(a) + parseInt(b), 0)) * 100);
                    progressBar.style.width = progressPercentage + '%';
                    progressText.textContent = numQuestionsGenerated + '/' + (numQuestionTypesPerType.reduce((a, b) => parseInt(a) + parseInt(b), 0));

                    // Add the generated question to the generated_questions array
                    generated_questions.push(data);

                    // Check if all questions have been generated
                    if (numQuestionTypesPerType.reduce((a, b) => parseInt(a) + parseInt(b), 0) == generated_questions.length) {
                        // All questions have been generated, so display them on the page
                        for (let k=0; k < generated_questions.length; k++) {
                            let data=generated_questions[k];

                            // Create a container div element for the question and answer
                            var containerDiv=document.createElement('div');
                            containerDiv.className='p-5 bg-primary-subtle rounded-5 my-3';
                            outputDiv.appendChild(containerDiv);

                            // Create a p element for the question
                            var questionP=document.createElement('p');
                            questionP.textContent=data.question;
                            containerDiv.appendChild(questionP);

                            if (data.type_of_question == 'open question') {
                                // Create a textarea element for user input
                                var textarea = document.createElement('textarea');
                                textarea.style.width = '100%';
                                textarea.style.boxSizing = 'border-box';
                                textarea.rows = 4;
                                containerDiv.appendChild(textarea);

                                // Create a submit button for user input
                                var submitButton=document.createElement('button');
                                submitButton.type='button';
                                submitButton.className='btn btn-secondary my-2';
                                submitButton.style.marginTop='10px';
                                submitButton.textContent='Submit';
                                containerDiv.appendChild(submitButton);

                                // Add an event listener to the submit button
                                submitButton.addEventListener('click', (function(containerDiv) {
                                    return function() {
                                        var guess = textarea.value;
                                        var question = data.question;
                                        var answer = data.answer;
                                        fetch('/open_question_check_answer', {
                                            method: 'POST',
                                            headers: {
                                                'Content-Type': 'application/json'
                                            },
                                            body: JSON.stringify({ guess: guess, question: question, answer: answer })
                                        })
                                            .then(response => response.json())
                                            .then(data => {
                                                var answerP = document.createElement('p');
                                                answerP.textContent = data.response;
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
                                                    answerP.className = 'answer';
                                                    answerP.textContent = data.response;
                                                    containerDiv.appendChild(answerP);
                                                    if (data.response.startsWith("Correct")) {
                                                        this.style.backgroundColor = '#28a745';
                                                    } else {
                                                        this.style.backgroundColor = '#dc3545';
                                                    }
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
                                                    answerP.className = 'answer';
                                                    answerP.textContent = data.response;
                                                    containerDiv.appendChild(answerP);
                                                    if (data.response.startsWith("Correct")) {
                                                        this.style.backgroundColor = '#28a745';
                                                    } else {
                                                        this.style.backgroundColor = '#dc3545';
                                                    }
                                                });
                                        });
                                    })(containerDiv);
                                }
                            }
                        }
                    }

                    // Process the next item in the queue
                    processQueue();
                });
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

    });

});

document.addEventListener('DOMContentLoaded', function() {
    // Set up drag-and-drop functionality
    const draggables = document.querySelectorAll('.draggable');
    const dropzones = document.querySelectorAll('.dropzone');

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', function(event) {
            event.dataTransfer.setData("text", event.target.id);
        });
    });

    dropzones.forEach(dropzone => {
        dropzone.addEventListener('dragover', function(event) {
            event.preventDefault();
        });

        dropzone.addEventListener('drop', function(event) {
            event.preventDefault();
            const id = event.dataTransfer.getData("text");
            const draggable = document.getElementById(id);
            if (!dropzone.querySelector('.draggable')) {
                dropzone.appendChild(draggable);
                const inputField = document.getElementById('input-' + dropzone.id);
                if (inputField) {
                    inputField.value = id;  // Update the corresponding hidden input with the draggable ID
                }
            }
        });
    });

    // Fetch questions from the server
    fetchQuestions();

    // Handle form submission for drag-and-drop
    const form = document.getElementById('drag-drop-form'); // Assuming the ID of your form
    form.onsubmit = function(event) {
        event.preventDefault(); // Prevent form from submitting normally

        // Collect data from the form
        let formData = {
            'image1': document.getElementById('dropzone1').getAttribute('data-value'),
            'image2': document.getElementById('dropzone2').getAttribute('data-value'),
            'image3': document.getElementById('dropzone3').getAttribute('data-value')
        };

        // Send data using fetch (AJAX)
        fetch('/show_question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(formData)
        }).then(response => response.json())
          .then(data => {
              // Handle response data
              document.getElementById('feedback').textContent = data.feedback;
              // Update score and other UI elements as needed
              // Update correct/incorrect styles based on data.correct_flags
          });
    };

    // Add event listener for submitting answers for MCQs
    document.getElementById('submit').addEventListener('click', submitAnswer);

    // Add event listener for displaying the next question
    document.getElementById('next').addEventListener('click', displayNextQuestion);
});

let quizQuestions = [];
let currentQuestionIndex = 0;

// Function to fetch questions from the server
function fetchQuestions() {
    fetch('/api/quiz')
        .then(response => response.json())
        .then(data => {
            quizQuestions = data;
            displayQuestion();
        });
}

// Function to display the current question
function displayQuestion() {
    const question = quizQuestions[currentQuestionIndex];
    const questionContainer = document.getElementById('question');
    const optionsContainer = document.getElementById('options');
    
    questionContainer.innerHTML = `<h2>${question.question}</h2>`;
    optionsContainer.innerHTML = '';
    if (question.options) {
        question.options.forEach((option, index) => {
            const radioHtml = `<label>
                <input type="radio" name="option" value="${option}">
                ${option}
            </label><br>`;
            optionsContainer.innerHTML += radioHtml;
        });
    }
    document.getElementById('feedback').innerHTML = '';
    document.getElementById('next').style.display = 'none';
}

// Function to submit the answer and display feedback
function submitAnswer() {
    const selectedOption = document.querySelector('input[name="option"]:checked');
    if (selectedOption) {
        const selectedValue = selectedOption.value;
        const question = quizQuestions[currentQuestionIndex];
        const correctAnswer = question.answer;
        const feedbackContainer = document.getElementById('feedback');
        if (selectedValue === correctAnswer) {
            feedbackContainer.innerHTML = '<p>Correct!</p>';
        } else {
            feedbackContainer.innerHTML = `<p>Incorrect. The correct answer is: ${correctAnswer}</p>`;
        }
        document.getElementById('next').style.display = 'block';
    }
}

// Function to display the next question
function displayNextQuestion() {
    if (currentQuestionIndex < quizQuestions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    } else {
        document.getElementById('quiz-container').innerHTML = '<h1>Quiz Completed!</h1>';
    }
}

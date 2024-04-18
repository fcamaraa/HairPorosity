let score = 0;

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var dropTarget = ev.target.closest('.dropzone');
    if (dropTarget && !dropTarget.querySelector('.draggable')) {
        dropTarget.appendChild(document.getElementById(data));
    }
}

document.querySelectorAll('.draggable').forEach(item => {
    item.addEventListener('dragstart', drag);
});

document.querySelectorAll('.dropzone').forEach(item => {
    item.addEventListener('dragover', allowDrop);
    item.addEventListener('drop', drop);
});

document.addEventListener('DOMContentLoaded', function() {
    var submitBtn = document.getElementById('submitBtn');
    submitBtn.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent default form submission
        if (!this.classList.contains('clicked')) {
            submitAnswer();  // Evaluate drag-and-drop answers
            this.classList.add('clicked');
            this.textContent = 'Next';  // Change button text to 'Next'
        } else {
            // Navigate to the next URL on second click
            window.location.href = this.getAttribute('data-next-url');
        }
    });
});

function submitAnswer() {
    const correctAssignments = {
        'image1': 'low',
        'image2': 'medium',
        'image3': 'high'
    };
    let localScore = 0;  // Track correct answers locally
    document.querySelectorAll('.dropzone').forEach(zone => {
        let child = zone.querySelector('.draggable');
        if (child && correctAssignments[zone.id] === child.id) {
            localScore++;
        }
    });
    score += localScore;
    alert('Your score: ' + localScore + '/3');  // Display score for this round
}

$(document).ready(function() {
    const inputField = $('input#searchInput');
    const learningPathButton = $('.buttons button#pathButton');
    const courseButton = $('.buttons button#courseButton');

    // Disable buttons initially
    learningPathButton.prop('disabled', true);
    courseButton.prop('disabled', true);

    inputField.on('input', function() {
        const inputValueLength = inputField.val().length;
        learningPathButton.prop('disabled', inputValueLength < 3);
        courseButton.prop('disabled', inputValueLength < 3);
    });

    // Handle button click events
    learningPathButton.on('click', function() {
        generateLearningPath(inputField.val());
    });

    courseButton.on('click', function() {
        generateCourse(inputField.val());
    });
});

function generateLearningPath(text) {
    $.ajax({
        url: '/api/generate_learningpath',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ text: text, user_id: userId }),
        success: function(data) {
            Swal.fire({
                icon: 'success',
                title: 'Learning path generated successfully!',
                showConfirmButton: false,
                timer: 1500
            }).then(() => {
                const pathId = data.id;
                window.location.href = `/learningpath/${pathId}`;
            });
        },
        error: function(xhr, status, error) {
            console.error('Error generating the learning path:', error);
            Swal.fire({
                icon: 'error',
                title: 'Failed to generate the learning path',
                text: 'Please try again later'
            });
        }
    });
}

function generateCourse(text) {
    $.ajax({
        url: '/api/generate_courses',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ text: text, user_id: userId }),
        success: function(data) {
            Swal.fire({
                icon: 'success',
                title: 'Course generated successfully!',
                showConfirmButton: false,
                timer: 1500
            }).then(() => {
                const courseId = data.id;
                window.location.href = `/course/${courseId}`;
            });
        },
        error: function(xhr, status, error) {
            console.error('Error generating the course:', error);
            Swal.fire({
                icon: 'error',
                title: 'Failed to generate the course',
                text: 'Please try again later'
            });
        }
    });
}
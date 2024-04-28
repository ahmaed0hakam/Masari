// Function to generate lessons for a course
function generateLessons(courseTitle, courseId) {

    $('#loader-container').css('display', 'flex');
    // Make AJAX request to generate lessons for the course
    $.ajax({
        url: '/api/generate_lessons',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ course_title: courseTitle, course_id: courseId, user_id: userId }),
        success: function(data) {

            $('#loader-container').hide();
            Swal.fire({
                icon: 'success',
                title: 'Lessons generated successfully!',
                showConfirmButton: false,
                timer: 1500
            }).then(() => {
                const courseId = data.id;
                const courseTitle = encodeURIComponent(data.course_title); // Encode the course title

                window.location.href = `/course/${courseId}/${courseTitle}`;
            });
        },
        error: function(xhr, status, error) {
            $('#loader-container').hide();
            Swal.fire({
                icon: 'error',
                title: 'Failed to generate lessons',
                text: 'Please try again later'
            });
        }
    });
}

// Add event listener to Generate Lessons buttons
$(document).ready(function() {
    $('.generate-lessons').on('click', function() {
        // Retrieve the course title from the data attribute of the button
        const courseTitle = $(this).data('course-title');
        const courseId = $(this).data('course-id');
        generateLessons(courseTitle, courseId); // Call generateLessons with the course title
    });
});
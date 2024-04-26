// Function to generate lessons for a course
function generateLessons(lessonTitle, lessonId) {

    $('#loader-container').css('display', 'flex');
    // Make AJAX request to generate lessons for the course
    $.ajax({
        url: '/api/generate_content',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ lesson_title: lessonTitle, lesson_id: lessonId, user_id: userId }),
        success: function(data) {

            $('#loader-container').hide();
            Swal.fire({
                icon: 'success',
                title: 'Lesson generated successfully!',
                showConfirmButton: false,
                timer: 1500
            }).then(() => {
                const content = data.content;
                const $contentArea = $('.content-area');
                $contentArea.text(content);
               
            });
        },
        error: function(xhr, status, error) {
            $('#loader-container').hide();
            Swal.fire({
                icon: 'error',
                title: 'Failed to generate lesson',
                text: 'Please try again later'
            });
        }
    });
}

// Add event listener to Generate Lessons buttons
$(document).ready(function() {
    $('.generate-lesson-content').on('click', function() {
        // Retrieve the course title from the data attribute of the button
        const lessonTitle = $(this).data('lesson-title');
        const lessonId = $(this).data('lesson-id');
        generateLessons(lessonTitle, lessonId); // Call generateLessons with the course title
    });
});
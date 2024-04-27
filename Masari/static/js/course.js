// Function to generate lessons for a course
function generateLessons(lessonTitle, lessonId) {

    $('#loader-container').css('display', 'flex');
    // Make AJAX request to generate lessons for the course
    $.ajax({
        url: '/api/generate_content',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ lesson_title: lessonTitle, lesson_id: lessonId, course_title: courseTitle, user_id: userId }),
        success: function(data) {
            $('.chat-widget').show();

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
                const $lessonTitle = $('.lesson-title');
                $lessonTitle.text(lessonTitle);
               
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


function sendChat(lastChat) {
    var firstLessonId = null; // Initialize variable to store the first lessonId

    // Iterate over elements with class .generate-lesson-content
    $('.generate-lesson-content').each(function(index, element) {
        if (index === 0) { // Check if it's the first element
            // Get the lessonId attribute from the first element
            firstLessonId = $(element).data('lesson-id');
            return false; // Exit the loop after retrieving the first lessonId
        }
    });

    if (firstLessonId !== null) {
        // Make AJAX request using the first lessonId
        $.ajax({
            url: '/api/generate_reply',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ user_input: lastChat, lesson_id: firstLessonId }),
            success: function(data) {
                // Append the reply to the chat widget body
                $('.chat-widget-body').append('<p style="align-self: flex-end;">' + data.reply + '</p>');
            },
            error: function(xhr, status, error) {
                // Handle error if AJAX request fails
                console.error('Error:', error);
            }
        });
    } else {
        console.error('No lessonId found.');
    }
}


// Add event listener to Generate Lessons buttons
$(document).ready(function() {

    $('.chat-widget').hide(); // Hide the chatbot widget if no text in .content-area

    $('.generate-lesson-content').on('click', function() {
        // Retrieve the course title from the data attribute of the button
        const lessonTitle = $(this).data('lesson-title');
        const lessonId = $(this).data('lesson-id');
        var contentText = $('.content-area').text();
        
        generateLessons(lessonTitle, lessonId); // Call generateLessons with the course title
    });

    $('.send-chat').click(function() {
        // Get the value from the input field
        var message = $('.chat-widget-input input').val();
    
        // Clear the input field after retrieving its value
        $('.chat-widget-input input').val('');
    
        // Append the message as a new <p> element inside .chat-widget-body
        $('.chat-widget-body').append('<p>' + message + '</p>');

        sendChat(message);
    });
});
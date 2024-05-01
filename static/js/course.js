function generateLessons(lessonTitle, lessonId) {

    $('#loader-container').css('display', 'flex');
    $.ajax({
        url: '/api/generate_content',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ lesson_title: lessonTitle, lesson_id: lessonId, course_title: courseTitle, user_id: userId }),
        success: function (data) {
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
                $contentArea.html(content);
                const $lessonTitle = $('.lesson-title');
                $lessonTitle.text(lessonTitle);

            });
        },
        error: function (xhr, status, error) {
            $('#loader-container').hide();
            Swal.fire({
                icon: 'error',
                title: 'Failed to generate lesson',
                text: 'Please try again later'
            });
        }
    });
}

function scrollChatToBottom() {
    var chatWidgetBody = $('.chat-widget-body');
    if (chatWidgetBody.length > 0) {
        chatWidgetBody.animate({ scrollTop: chatWidgetBody.prop('scrollHeight') }, 300);
    }
}

function sendChat(lastChat, chatBubbleHTML) {
    var firstLessonId = null; // Initialize variable to store the first lessonId
    $('.chat-widget-body').append(chatBubbleHTML);
    $('.chat-widget-input').attr("disabled", "disabled");
    scrollChatToBottom();

    $('.generate-lesson-content').each(function (index, element) {
        if (index === 0) { // Check if it's the first element
            firstLessonId = $(element).data('lesson-id');
            return false;
        }
    });

    if (firstLessonId !== null) {

        $.ajax({
            url: '/api/generate_reply',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ user_input: lastChat, lesson_id: firstLessonId }),
            success: function (data) {
                $('.chat-widget-body .chat-bubble').last().remove();

                $('.chat-widget-body').append('<p class="chat-bubble" style="align-self: flex-start;">' + data.reply + '</p>');
                scrollChatToBottom();
            },
            error: function (xhr, status, error) {
                $('.chat-widget-body .chat-bubble').last().remove();

            }
        });
        $('.chat-widget-input').removeAttr("disabled");
    } else {
        console.error('No lessonId found.');
    }
}


// Add event listener to Generate Lessons buttons
$(document).ready(function () {

    $('.chat-widget').hide();

    $('.generate-lesson-content').on('click', function () {

        const lessonTitle = $(this).data('lesson-title');
        const lessonId = $(this).data('lesson-id');
        var contentText = $('.content-area').text();

        generateLessons(lessonTitle, lessonId);
    });

    $('.send-chat').click(function () {
        var message = $('.chat-widget-input input').val();

        $('.chat-widget-input input').val('');


        const chatBubbleHTML = `
    <div class="chat-bubble" style="align-self: flex-start;">
        <div class="typing">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    </div>
`;

        $('.chat-widget-body').append('<p class="chat-bubble human" style="align-self: flex-end;">' + message + '</p>');
        scrollChatToBottom();

        sendChat(message, chatBubbleHTML);
    });
});
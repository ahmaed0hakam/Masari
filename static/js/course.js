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
                var converter = new showdown.Converter();
                var html = converter.makeHtml(content);

                $contentArea.html(html);
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


$(document).ready(function () {

    controlChatBotApp();

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

    const startButton = $("#startBtn");
    const outputInput = $("#output"); // Assuming outputDiv is an <input> element

    if ("webkitSpeechRecognition" in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US"; // Set the language to English

        let timeoutId; // Variable to hold the timeout ID

        recognition.onstart = () => {
            startButton.css('background-color', '#FFA128');
            timeoutId = setTimeout(() => {
                recognition.stop(); // Stop recognition after timeout
            }, 2000); // Adjust timeout duration (e.g., 2000ms = 2 seconds)
        };

        recognition.onresult = (event) => {
            clearTimeout(timeoutId); // Clear timeout on new speech input
            let interimTranscript = "";
            let finalTranscript = "";

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + " ";
                } else {
                    interimTranscript += transcript;
                }
            }

            const finalOutput = `${interimTranscript}${finalTranscript}`;
            outputInput.val(finalOutput);

            // Restart timeout for detecting silence
            timeoutId = setTimeout(() => {
                recognition.stop(); // Stop recognition after timeout
            }, 2000); // Adjust timeout duration
        };

        recognition.onend = () => {
            // startButton.text("Start Recording");
            startButton.css('background-color', '#0097b2');
        };

        startButton.on("click", () => {
            if (recognition.start) {
                recognition.start();
            }
        });
    } else {
        // Display error message if Web Speech API is not supported
        outputInput.val("Web Speech API not supported in this browser.");
    }
    function controlChatBotApp () {
        const chatBody = $('.chat-widget-body');
        const chatInput = $('.chat-widget-input')

        if (chatBody.css('display') !== 'none') {
            chatBody.css('display', 'none');
            chatInput.css('display', 'none');
        } else {
            // If chat-widget-body is display none, show it as flex
            chatBody.css('display', 'flex');
            chatInput.css('display', 'flex');
        }
    }

    $('.chat-widget-header').on("click", () => {
        controlChatBotApp();
    });
});
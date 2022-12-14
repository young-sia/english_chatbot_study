function submit_message(project_name, message) {
        $.post( `/project/${project_name}/project_message`, {message: message}, handle_response);

        function handle_response(data) {
          // append the bot repsonse to the div
          $('.chat-container').append(`
                <div class="chat-message col-md-5 offset-md-7 bot-message">
                    ${data.message}
                </div>
          `)
          // remove the loading indicator
          $( "#loading" ).remove();
        }
    }
function input_audio(){
        let isRecording = false;
        let mediaRecorder = null;

        const mediaStream = await navigator.mediaDevices.getUserMedia({audio: true});
        mediaRecorder = new MediaRecorder(mediaStream);

}
$('#target').on('submit', function(e){
        e.preventDefault();
        const input_message = $('#input_message').val()
        //        const input_audio_message = $('#input_message').val()
        // return if the user does not enter any text
        if (!input_message) {
          return
        }

//        $('.chat-container').append(`
//            <div class="chat-message col-md-5 human-message">
//                    ${input_audio_message}
//                </div>
//        `)
        $('.chat-container').append(`
            <div class="chat-message col-md-5 human-message">
                ${input_message}
            </div>
        `)

        // loading
        $('.chat-container').append(`
            <div class="chat-message text-center col-md-2 offset-md-10 bot-message" id="loading">
                <b>...</b>
            </div>
        `)

        // clear the text input
        $('#input_message').val('')

        // send the message
        submit_message('example_project', input_message)
    });
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        // Add persistent properties
        mediaRecorder: null,
        audioChunks: [],
        
        toggleRecording: function(n_clicks, currentState) {
            let newState = !currentState;
            console.log("Recording state is now:", newState);
            
            if (newState) {
                navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
                    // Store the mediaRecorder on the clientside object
                    dash_clientside.clientside.mediaRecorder = new MediaRecorder(stream);
                    console.log("MediaRecorder initiated.");

                    dash_clientside.clientside.mediaRecorder.ondataavailable = event => {
                        if (event.data.size > 0) {
                            dash_clientside.clientside.audioChunks.push(event.data);
                        }
                    };
        
                    dash_clientside.clientside.mediaRecorder.onstop = () => {
                        console.log("Stopping MediaRecorder.");
                        const audioBlob = new Blob(dash_clientside.clientside.audioChunks, { type: "audio/wav" });
                        let formData = new FormData();
                        formData.append("audio", audioBlob, "recorded_audio.wav");
        
                        const xhr = new XMLHttpRequest();
                        xhr.open('POST', '/save_audio', true);
                        xhr.onload = function() {
                            if (xhr.status === 200) {
                                console.log('Audio file saved successfully.');
                                // Clean up the chunks after saving
                                dash_clientside.clientside.audioChunks = [];
                                console.log('Audio chunks cleaned.');
                            } else {
                                console.error('Error saving audio: ', xhr.statusText);
                            }
                        };
                        xhr.send(formData);
                        // Clear audioChunks again
                        dash_clientside.clientside.audioChunks = [];
                    };

                    dash_clientside.clientside.mediaRecorder.start();
                }).catch(error => console.error("Error accessing microphone", error));
            } else {
                // Access the persistent mediaRecorder
                if (dash_clientside.clientside.mediaRecorder && dash_clientside.clientside.mediaRecorder.state === 'recording') {
                    dash_clientside.clientside.mediaRecorder.stop();
                    const streamTracks = dash_clientside.clientside.mediaRecorder.stream.getTracks();
                    streamTracks.forEach(track => track.stop());
                    dash_clientside.clientside.mediaRecorder = null;
                }
            }
            return newState;
        }
    }
});

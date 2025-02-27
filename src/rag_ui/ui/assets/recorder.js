window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        // Add persistent properties
        mediaRecorder: null,
        audioChunks: [],
        isRecording: false,
        
        toggleRecording: function(n_clicks, currentState) {
            // Only proceed if n_clicks is valid (prevents initial call issues)
            if (!n_clicks) return [currentState, null, "fas fa-microphone"];
            
            // Toggle recording state
            let newState = !this.isRecording;
            this.isRecording = newState;
            
            if (newState) {
                // Start recording
                navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    this.audioChunks = []; // Clear previous chunks
                    this.mediaRecorder = new MediaRecorder(stream);
                    console.log("MediaRecorder initiated.");
                    
                    this.mediaRecorder.ondataavailable = event => {
                        if (event.data.size > 0) {
                            this.audioChunks.push(event.data);
                        }
                    };
                    
                    this.mediaRecorder.onstop = () => {
                        console.log("Stopping MediaRecorder.");
                        if (this.audioChunks.length === 0) {
                            console.log("No audio chunks to process");
                            return;
                        }
                        
                        const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
                        let formData = new FormData();
                        formData.append("audio", audioBlob, "recorded_audio.wav");
                        
                        const xhr = new XMLHttpRequest();
                        xhr.open('POST', '/save_audio', true);
                        xhr.onload = function() {
                            if (xhr.status === 200) {
                                try {
                                    const response = JSON.parse(xhr.responseText);
                                    const message = response.message;
                                    const code = response.code;
                                    const path = response.path;
                                    
                                    console.log(`Message: ${message}, Code: ${code}, Filename: ${path}`);
                                } catch (error) {
                                    console.error('Error parsing JSON response: ', error);
                                }
                            } else {
                                console.error('Error saving audio: ', xhr.statusText);
                            }
                        };
                        xhr.send(formData);
                    };
                    
                    this.mediaRecorder.start();
                })
                .catch(error => {
                    console.error("Error accessing microphone", error);
                    this.isRecording = false; // Reset recording state on error
                    return [false, null, "fas fa-microphone"];
                });
                
                return [true, "./src/rag_ui/data/audio/recorded_audio.wav", "fas fa-circle"];
            } else {
                // Stop recording
                if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
                    this.mediaRecorder.stop();
                    if (this.mediaRecorder.stream) {
                        const streamTracks = this.mediaRecorder.stream.getTracks();
                        streamTracks.forEach(track => track.stop());
                    }
                }
                
                return [false, "./src/rag_ui/data/audio/recorded_audio.wav", "fas fa-microphone"];
            }
        }
    }
});

var videoFeed = document.getElementById('video-feed'); // Change this to the actual video feed element ID

// Function to start the video feed
function startVideoFeed() {
    videoFeed.src = "{{ url_for('video_feed', action='start') }}";
}

// Function to stop the video feed
function stopVideoFeed() {
    videoFeed.src = "{{ url_for('video_feed', action='stop') }}";
}

// Handle leaving the page
window.addEventListener('beforeunload', function () {
    stopVideoFeed(); // Stop the video feed when leaving the page
    });

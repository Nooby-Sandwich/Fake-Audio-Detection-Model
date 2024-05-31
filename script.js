// scripts.js
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let formData = new FormData(this);
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.result;
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle the error, e.g., show an error message to the user
    });
});

/*function uploadAudio() {
    var formData = new FormData();
    var file = document.getElementById('customFile').files[0];
    formData.append('file', file);

    $.ajax({
        type: 'POST',
        url: '/predict',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            // Display the result
            $('#result').text('Result: ' + response.result);
        },
        error: function(xhr, status, error) {
            console.error(error);
            $('#result').text('An error occurred: ' + error);
        }
    });
}*/

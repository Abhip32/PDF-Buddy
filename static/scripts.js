
document.addEventListener("DOMContentLoaded", function() {
  var cards = document.getElementsByClassName("fade-in");

  // Add the "visible" class to each card with a delay
  for (var i = 0; i < cards.length; i++) {
    (function(index) {
      setTimeout(function() {
        cards[index].classList.add("visible");
      }, index * 200); // Adjust the delay (in milliseconds) between each card
    })(i);
  }
});

function handleFileSelectImg(event) {
    var previewContainer = document.getElementById('preview-container');
    previewContainer.innerHTML = '';

    var files = event.target.files;
    for (var i = 0; i < files.length; i++) {
        var file = files[i];

        // Create a FileReader instance
        var reader = new FileReader();

        // Closure to capture the file information
        reader.onload = (function (file) {
            return function (e) {
                // Create a new image element
                var image = document.createElement('img');
                image.src = e.target.result;
                image.classList.add('img-fluid');

                // Create a new column div
                var column = document.createElement('div');
                column.classList.add('col-md-4', 'col-sm-6', 'col-12', 'bg-light', 'm-3', 'p-3');

                // Create a heading element for the file name
                var fileName = document.createElement('h6');
                fileName.textContent = file.name;
                column.appendChild(fileName);
                column.appendChild(image);

                // Append the column to the container
                previewContainer.appendChild(column);
            };
        })(file);

        // Read the file as a data URL
        reader.readAsDataURL(file);
    }
}

 // Function to handle file selection and display the first page preview
 function handleFileSelect(event) {
    var previewContainer = document.getElementById('preview-container');
    previewContainer.innerHTML = '';

    var files = event.target.files;
    for (var i = 0; i < files.length; i++) {
        var file = files[i];

        // Create a FileReader instance
        var reader = new FileReader();

        // Closure to capture the file information
        reader.onload = (function (file) {
            return function (e) {
                // Create a new canvas element
                var canvas = document.createElement('canvas');
                var context = canvas.getContext('2d');

                // Load the PDF using PDF.js library
                pdfjsLib.getDocument(e.target.result).promise.then(function (pdf) {
                    // Fetch the first page of the PDF
                    pdf.getPage(1).then(function (page) {
                        var viewport = page.getViewport({ scale: 1.0 });
                        canvas.width = viewport.width;
                        canvas.height = viewport.height;

                        // Render the first page of the PDF onto the canvas
                        var renderContext = {
                            canvasContext: context,
                            viewport: viewport
                        };
                        page.render(renderContext).promise.then(function () {
                            // Create a new embed element
                            var preview = document.createElement('embed');
                            preview.src = canvas.toDataURL('image/jpeg');
                            preview.classList.add('img-fluid');
                            preview.setAttribute('sandbox', 'allow-same-origin allow-scripts');

                            // Create a new column div
                            var column = document.createElement('div');
                            column.classList.add('col-md-4', 'col-sm-6', 'col-12', 'bg-light','m-3','p-3');
                                                            // Create a heading element for the file name
                                                            var fileName = document.createElement('h6');
                            fileName.textContent = file.name;
                            column.appendChild(fileName);
                            column.appendChild(preview);

                            // Append the column to the container
                            previewContainer.appendChild(column);
                        });
                    });
                });
            };
        })(file);

        // Read the file as an ArrayBuffer
        reader.readAsArrayBuffer(file);
    }
}


function changePasswordVisibility() {
    const password = document.getElementById('password');
    const togglePassword = document.getElementById('togglePassword');

    if (password.getAttribute('type') === 'password') {
        //change to text
        password.setAttribute('type', 'text');
        togglePassword.classList.add('fa-eye-slash');
    } else {
        //change to password
        password.setAttribute('type', 'password');
        togglePassword.classList.remove('fa-eye-slash');
    }
}


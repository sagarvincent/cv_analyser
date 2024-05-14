function displayUploadedFiles(dropZoneId, fileListId, fileInputId) {
    const fileList = document.getElementById(fileListId);
    fileList.innerHTML = ''; // Clear previous content

    const files = document.getElementById(fileInputId).files;
    if (files.length > 0) {
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const fileName = file.name;
            const listItem = document.createElement('div');
            listItem.textContent = fileName;
            fileList.appendChild(listItem);
        }
    } else {
        fileList.textContent = 'No files uploaded';
    }
}

// Function to handle drag and drop functionality
function handleFileDrop(event, dropZoneId, fileListId, fileInputId) {
    event.preventDefault();
    const files = event.dataTransfer.files;
    const fileInput = document.getElementById(fileInputId);
    fileInput.files = files;

    // Display uploaded files
    displayUploadedFiles(dropZoneId, fileListId, fileInputId);
}

// Function to handle file input change event
function handleFileInputChange(dropZoneId, fileListId, fileInputId) {
    displayUploadedFiles(dropZoneId, fileListId, fileInputId);
}

// Add event listeners for drag and drop functionality and file input change event
document.getElementById('drop-zone1').addEventListener('dragover', function(event) {
    event.preventDefault();
});

document.getElementById('drop-zone1').addEventListener('drop', function(event) {
    handleFileDrop(event, 'drop-zone1', 'fileList1', 'fileInput1');
});

document.getElementById('fileInput1').addEventListener('change', function() {
    handleFileInputChange('drop-zone1', 'fileList1', 'fileInput1');
});


// Add event listeners for drag and drop functionality and file input change event
document.getElementById('drop-zone2').addEventListener('dragover', function(event) {
    event.preventDefault();
});

document.getElementById('drop-zone2').addEventListener('drop', function(event) {
    handleFileDrop(event, 'drop-zone2', 'fileList2', 'fileInput2');
});

document.getElementById('fileInput2').addEventListener('change', function() {
    handleFileInputChange('drop-zone2', 'fileList2', 'fileInput2');
});
tbody = document.getElementById("table-body");
// const table = document.getElementById("table");



function deleteFile(button) {
    var result = confirm("Want to delete?");
    if (result) {

        const formData = new FormData();

        // Get the name of the file from the table row
        var text = button.parentNode.parentNode.parentNode.cells[2].textContent;
        var fileName = text.split('.Xlsx')[0];
        console.log(fileName);

        // Construct the URL for the file download
        var url = "/delete_file/" + encodeURIComponent(fileName);

        // Navigate to the file download URL
        window.location.href = url;
    }
}

function downloadFile(button) {
    const formData = new FormData();

    // Get the name of the file from the table row
    var text = button.parentNode.parentNode.parentNode.cells[2].textContent;
    var fileName = text.split('.Xlsx')[0];
    console.log(fileName);

    // Construct the URL for the file download
    var url = "/download_file/" + encodeURIComponent(fileName);

    // Navigate to the file download URL
    window.location.href = url;
}

function fileSize(size) {

    let file_size;
    const units = ["B", "KB", "MB", "GB", "TB"];
    let unitIndex = 0;

    while (size >= 1024) {
        size /= 1024;
        unitIndex++;
    }

    file_size = size.toFixed(2) + " " + units[unitIndex];

    return file_size;
}


function display_files() {
    tbody.innerHTML = "";
    try {
        fetch('/file_info').then(response => response.json()).then(data => {
            for (file in data) {
                fInfo = data[file];

                // Creating a new row
                tr = tbody.insertRow(-1);

                // Filling up the row
                trCell = tr.insertCell(-1);
                trCell.appendChild(createNewCheckbox(file))
                // trCell.createNewCheckboxt
                // trCell.innerHTML = `<td><input type="checkbox" class="checkbox_"></td>`

                trCell = tr.insertCell(-1);
                trCell.innerHTML = `<td style="text-align: center;"><i class="fa fa-file-excel" aria-hidden="true"
                id="excel_icon"></i></td>`

                trCell = tr.insertCell(-1);
                trCell.innerHTML = file;
                trCell.innerHTML += `</br>`;
                fSize = fileSize(fInfo['size']);
                trCell.innerHTML += fSize;

                trCell = tr.insertCell(-1);
                trCell.innerHTML = `<td>Operator X</td>`;

                trCell = tr.insertCell(-1);
                trCell.innerHTML = fInfo['upload_date'];
                trCell.innerHTML += `</br>`;
                trCell.innerHTML += fInfo['upload_time'];

                trCell = tr.insertCell(-1);
                trCell.innerHTML = `<td style="text-align: right !important;"><button class="icon_download_button"><i class="fa fa-arrow-down" aria-hidden="true" onclick="downloadFile(this)"></i></button></td>`;
                trCell.style.setProperty('text-align', 'right');

                trCell = tr.insertCell(-1);
                trCell.innerHTML = `<td style="text-align: right !important;"><button class="icon_download_button"><i class="fa fa-trash" aria-hidden="true" onclick="deleteFile(this)"></i></button></td>`;
                trCell.style.setProperty('text-align', 'right');
            }
        })
    } catch (error) {
        console.log(error);
    }
}

function createNewCheckbox(name) {
    var checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = name;
    checkbox.classList.add('ckb');
    // checkbox.id = id;
    return checkbox;
}




display_files();

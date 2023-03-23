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

function revertFile(button){
    const formData = new FormData();

    // GFeeting the name of the file
    var text = button.parentNode.parentNode.parentNode.cells[2].textContent;
    var fileName = text.split('.Xlsx')[0];
    console.log(fileName);

    // Construct the URL for the file download
    var url = "/revert/" + encodeURIComponent(fileName);
  
    // Navigate to the file download URL
    window.location.href = url;
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

function fileSize(size){
    
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


function display_files(){
    tbody.innerHTML = "";
    try{
        fetch('/file_info_previously').then(response => response.json()).then(data => {
            for(file in data){
                fInfo = data[file];
                
                // Creating a new row
                tr = tbody.insertRow(-1);

                // Filling up the row
                trCell = tr.insertCell(-1);
                trCell.appendChild(createNewCheckbox(file));

                trCell = tr.insertCell(-1);
                trCell.innerHTML = `<td style="text-align: center;"><i class="fa fa-file-excel" aria-hidden="true"
                id="excel_icon_old"></i></td>`

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
                trCell.innerHTML = `<td><button class="icon_download_button"><i class="fa fa-arrow-down" aria-hidden="true" onclick="downloadFile(this)"></i></button></td>`;

                trCell = tr.insertCell(-1);
                trCell.innerHTML = `<td><button class="icon_download_button"><i class="fa fa-trash" aria-hidden="true" onclick="deleteFile(this)"></i></button></td>`;
                
                trCell = tr.insertCell(-1);
                trCell.innerHTML = `<td><button class="icon_download_button"><i class="fa fa-undo" aria-hidden="true" onclick="revertFile(this)"></i></button></td>`;
            }
        })
    } catch (error){
        console.log(error);
    }
}

function createNewCheckbox(name){
    var checkbox = document.createElement('input'); 
    checkbox.type= 'checkbox';
    checkbox.name = name;
    checkbox.classList.add('ckb');
    // checkbox.id = id;
    return checkbox;
}

document.getElementById('btn').onclick = function() {
    // Collect the name of all the files selected (name format e.g operator1.xlsx is returned)
    let formData = new FormData();
    var markedCheckbox = document.querySelectorAll('input[type="checkbox"]:checked'); // Collects all checked checkboxes
    
    // Creating a formData with all the files checked
    for (var checkbox of markedCheckbox) {
        formData.append('fileslist', checkbox.name);
    }

    // Displaying a load page
    filesArea = document.querySelector(".centered")
    filesArea.innerHTML = `
    <div class="upload_container">
        <div class="response_box">
            <div class="file-area">
                </br><div class="load_icon"><i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i></div>
                </br><header>Processing...</header>     
            </div>
        </div>
    </div>`;


    // Sending a fetch to combine selected files only
    setTimeout(function(){
    try{
        fetch('/combine_selected', {
            method: 'POST',
            body: formData,
        })
    } catch (error){
        console.error(error);
    }
    window.location.href='success_admin';
    }, 2000);
}

document.getElementById('btn1').onclick = function(){

    // Collect the names of all the files selected
    let files = [];
    let formData = new FormData();
    var markedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    let link = document.createElement('a');
    link.href = '/download_file/';

    // Creating a formData with all files selected
    for (var checkbox of markedCheckboxes){
        link.href = '/download_file/' + checkbox.name;
        // link.download = checkbox.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}


display_files();
//selecting all required elements
const dropArea = document.querySelector(".drag-area"),
dragText = dropArea.querySelector("header"),
button = dropArea.querySelector("button"),
input = dropArea.querySelector("input");

area = document.querySelector(".centered")

const button_validate = document.querySelector(".upload-validate");
const cancel_icon = document.querySelector(".btn-cancel");

let file; //this is a global variable and we'll use it inside multiple functions
var error_logs;

button.onclick = ()=>{
  input.click(); //if user click on the button then the input also clicked
}

input.addEventListener("change", function(){
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); //calling function
});


//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0];
  showFile(); //calling function
});


function display_errors(data, tbody){
  tbody.innerHTML = "";
  try{
    for(eror in data){
        errInfo = data[eror];
        
        // Creating a new row
        tr = tbody.insertRow(-1);

        // Filling up the row
        trCell = tr.insertCell(-1);
        trCell.innerHTML = errInfo['line'];

        trCell = tr.insertCell(-1);
        trCell.innerHTML = errInfo['column'];

        trCell = tr.insertCell(-1);
        trCell.innerHTML = errInfo['error'];

      }
  } catch (error){
      console.log(error);
  }
}


function pythonSend(){
  // ----------- Excel validation and saving and allowing it to load while it validates --------- 
  const formData = new FormData();
  formData.append('file', file)
  console.log("Inside the pythonSend function")
  area.innerHTML = `
  <div class="upload_container">
      <div class="response_box">
        <form action="#">
          </br><div class="load_icon"><i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i></div>
          </br><header>Processing...</header>     
        </form>
      </div>
    </div>`;
  setTimeout(async function(){
    try{
      fetch('/uploader', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        body: formData, // body data type must match "Content-Type" header
      }).then(response => response.json()).then(data => {
        var count = Object.keys(data).length;

        // This is for looping through each individual error record
        for (err in data){
          console.log(data[err])
        }

        if (count == 0 ){
          window.location.href='success';
        } else {
          area.innerHTML = `
            <div class="error_container">
            <form method="get" action="file.doc"></form>
        <div class="checkmark_response_error">
          <i class="fas fa-exclamation-triangle"></i>
        </div>
        <h2 class="error_heading">File format is not correct</h2>
        </br>
        </br><span class="error_heading_small">Kindly fix the below errors</span>
        <div class="table-area-error">
            <table id="table">
              <thead>
                <tr>
                  <th>Line</th>
                  <th>Column</th>
                  <th>Error</th>
                </tr>
              </thead>
              <tbody id="table-body">
              </tbody>
            </table>
            </br>
          </div>
          <div class="admin_lower_container_error">
            <button class="aggergate_button" type="submit" onclick="window.location.href='upload'">Upload Again</button>
          </div>
          </form>
          </div>`;
          tbody = document.getElementById("table-body");
          display_errors(data, tbody);
        }
      });
    } catch (error) {
      console.error(error);
    }
    // window.location.href = "/validate_response";
  }, 1000);
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






function showFile(){
  let fileType = file.type; //getting selected file type
  let validExtensions = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]; //adding some valid image extensions in array
  let displaysize = fileSize(file.size);

  if(validExtensions.includes(fileType)){ //if user selected file is an image file
    let fileReader = new FileReader(); //creating new FileReader object
    fileReader.onload = ()=>{
      //let fileURL = fileReader.result; //passing user file source in fileURL variable
      
      let excelfileDiv = `<div class="btn-cancel" ><a href="upload.html" class="btn_cancel_upload"><i class="fa fa-times-circle" aria-hidden="true"></i></a></div><div class="icon-text"><div class="icon"><i class="fas fa-file-excel"></i></div><div>${file.name}</br>${displaysize}</div></div>`; //creating an img tag and passing user selected file source inside src attribute
      dropArea.innerHTML = excelfileDiv; //adding uploaded excel name inside dropArea container
      let buttonDiv =`<input type="button" value="Validate" class="validate-link" onclick = "pythonSend()">`;
      button_validate.innerHTML = buttonDiv; //adding validation button 
      // cancel_icon.style.display = "block !important;";
      // let cancelDiv = `<a href="upload.html" class="btn_cancel_upload"><i class="fa fa-times-circle" aria-hidden="true"></i></a>`;
      // cancel_icon.innerHTML = cancelDiv; //adding cancel button 
    }
    fileReader.readAsDataURL(file);
  }else{
    alert("This is not an excel File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}


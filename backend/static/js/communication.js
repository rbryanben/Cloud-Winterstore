//this is the global server url
let serverURL = window.location.origin;


function postToServer(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(xmlhttp.response);
        }
    }

    xmlhttp.open("POST", serverURL + url)
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.send(JSON.stringify(data));

}


function updateToServer(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(xmlhttp.response);
        }
    }

    xmlhttp.open("UPDATE", serverURL + url)
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.send(JSON.stringify(data));

}


function deleteToServer(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(xmlhttp.response);
        }
    }

    xmlhttp.open("DELETE", serverURL + url)
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.send(JSON.stringify(data));

}



function getFromServer(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(xmlhttp.response);
        }
    }

    xmlhttp.open("GET", serverURL + url)
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.send(JSON.stringify(data));

}



function putToServer(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(xmlhttp.response);
        }
    }

    xmlhttp.open("PUT", serverURL + url)
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.send(JSON.stringify(data));

}



 //function downloads a file
 let currentlyDownloading = false
 let xhttp = new XMLHttpRequest();

 function downloadFile(data,filename){
    if (currentlyDownloading){
        ShowWarning("Multiple Download Unsupported")
        return
    }
    showDownloads()
    currentlyDownloading = true
    //add object to download list
    var downloadList = document.querySelector(".downloads-list")
    var elementFrame = `<div id="${filename}download" class="download-item">
    <div class="download-item-header"> <span onclick="cancelCurrentDownload()" class="download-cancel">Cancel</span><i class="fas fa-file-download"></i><span style="margin-left: 5px;">${filename}</span></div>
    <div class="download-bar"><div id="${filename}progress" class="download-progress"></div></div>
    </div>`

    downloadList.innerHTML = elementFrame ;
    var downloadObject = document.getElementById(filename+"download")
    var progressObject = document.getElementById(filename+"progress")
   
    xhttp.onreadystatechange = function() {
        var a;
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            currentlyDownloading = false
            downloadList.innerHTML = ""
            setTimeout(()=>{
                hideDownloads()
            },1000)
            // Trick for making downloadable link
            a = document.createElement('a');
            a.href = window.URL.createObjectURL(xhttp.response);
            // Give filename you wish to download
            a.download = filename;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
        }
       
    };

    //get precentage 
    xhttp.addEventListener("progress",(e)=>{
        var precentage = (e.loaded / e.total) * 100 ;
        progressObject.style.width = precentage + "%"
    })

    // Post data to URL which handles post request
    xhttp.open("POST", "/console/get-file");
    xhttp.setRequestHeader("Content-Type", "application/json");
    // You should set responseType as blob for binary responses
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify(data));
}

function cancelCurrentDownload(){
    xhttp.abort();
    currentlyDownloading = false
    document.querySelector(".downloads-list").innerHTML = ""
    setTimeout(()=>{
        hideDownloads()
    },1000)
}

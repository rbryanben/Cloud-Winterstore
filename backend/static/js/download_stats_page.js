//this is the variable that holds the page browser
let downloadsPageBrowser 

//this is the class for download stats
let downloadStat = class {
    constructor(object){
        /// id name username data and downloads
        this.username = (object['user']['username']);
        this.id = (object['file']['id']);
        this.name = (object['file']['name']);
        this.date = convertDate(object['downloaded']);
        this.total = (object['totalDownloads']);

        //check if the file was downloaded 
        //rather by a client
        if (object["developerClient"] != null){
            this.username = object["developerClient"];
            this.username = this.username.substring(0,this.username.indexOf("@") - 1);
        }
        

        //trimmers 
        this.trimName()
        this.trimID()
    }

    trimName(){
        if (this.name.length > 25){
            this.name =  this.name.substring(0, 25) + "..."
        }
    }

    trimID(){
       this.id = this.id.substring(0, 25) + "..." + this.id.substring(46, 64)
    }

}

//set the page when the document has loaded
window.addEventListener("DOMContentLoaded",()=>{
    downloadsPageBrowser = document.querySelector(".browser-downloads-page")
})

//Show page (Entry)
function showBrowserDownloadPage(){
    downloadsPageBrowser.style.display = "block"

    //check if there is text in the search input
    //if yes then search for that string instead of getting all objects
    var search_input_string = document.getElementById("downloadFileSearchInput").value
    if (search_input_string.length > 0){
        searchDownloadStats()
    }
    else{
        getDownloadStats()
    }
}

//Hide page
function hideBrowserDownloadPage(){
    downloadsPageBrowser.style.display = "none"
}

//Refresh Page Function
function download_stats_page_refresh(object){
    //animate refresh button once
    if (!object.classList.contains("animate")){
        object.classList.add("animate")
    }
    else {
        object.classList.remove("animate")
    }
    showBrowserDownloadPage()
}

//get objects 
function getDownloadStats(){
    //start loading 
    set_download_stats_loading(true)

    //body to add objects
    var bodyToAdd = document.getElementById("bodydownloadFiles")
    bodyToAdd.innerHTML = ""
    
    //data to post
    data = {
        "project" : localStorage.getItem("working-project")
    }
    postToServer("/console/get-download-stats", data, function(responce) {
        //hide loading 
        set_download_stats_loading(false)
        if (responce == "500" || responce == "not found" || responce == "denied") {
            ShowWarning("Fetch Objects Failed")
        } else {
            //make json objects
            downloadedFilesArray = JSON.parse(responce)

            //for objects
            downloadedFilesArray.forEach(object => {
                //frame
                var downloadItem = new downloadStat(object)
                //frame
                var frame = 
                `
                <!-- download file-->
                <div class="download-file-item">
                    <div class="categorizer-text hide-mobile">${downloadItem.id}</div>
                    <div class="categorizer-text">${downloadItem.name}</div>
                    <div class="categorizer-text hide-mobile ">${downloadItem.username}</div>
                    <div class="categorizer-text hide-mobile ">${downloadItem.date}</div>
                    <div class="categorizer-text hide-mobile ">${downloadItem.total}</div>
                </div>
                `
                bodyToAdd.innerHTML += frame
            });
        }
    })

}

function searchDownloadStats(){
    if (document.getElementById("downloadFileSearchInput").value == ""){
        getDownloadStats()
    }
    
    //check if length of string to search is less than 63
    //in that case prevent search
    if (document.getElementById("downloadFileSearchInput").value.length < 63){
        return
    }

    //body to add 
    var bodyToAdd = document.getElementById("bodydownloadFiles")
    bodyToAdd.innerHTML = ""
    //data to post
    data = {
        "project" : localStorage.getItem("working-project"),
        "criteria" : document.getElementById("downloadFileSearchInput").value
    }
    postToServer("/console/search-download-stats", data, function(responce) {
        if (responce == "500" || responce == "not found" || responce == "denied") {
            //Do nothing
        } else {
            //make json objects
            downloadedFilesArray = JSON.parse(responce)

            //for objects
            downloadedFilesArray.forEach(object => {
                //frame
                var downloadItem = new downloadStat(object)
                //frame
                var frame = 
                `
                <!-- download file-->
                <div class="download-file-item">
                    <div class="categorizer-text">${downloadItem.id}</div>
                    <div class="categorizer-text">${downloadItem.name}</div>
                    <div class="categorizer-text hide-mobile ">${downloadItem.username}</div>
                    <div class="categorizer-text hide-mobile ">${downloadItem.date}</div>
                    <div class="categorizer-text hide-mobile ">${downloadItem.total}</div>
                </div>
                `
                bodyToAdd.innerHTML += frame
            });
        }
    })
}

//loading 
function set_download_stats_loading(status){
    var loader = document.getElementById("downloadFilesLoader")
    //if status is true show loading 
    if (status){
        if (!loader.classList.contains("show")){
            loader.classList.add("show")
        }
        return
    }
    //if status is false
    loader.classList.remove("show")
}

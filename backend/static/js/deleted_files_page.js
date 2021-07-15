//This varibale holds the page
let deletedPageBrowser 

//class to hold deleted objects
let deletedFile = class {
    constructor(jsonObject){
        this.id = jsonObject["fileID"]
        this.name = jsonObject["name"]
        this.deleted_by = jsonObject["deletedBy"]
        this.deleted = jsonObject["deleted"]
        this.trimedID = jsonObject["fileID"]

        //trim name 
        this.trimName()
        this.trimID()
        this.convertDate()
        this.trimDeletedBy()
    }

    trimDeletedBy(){
        if (this.deleted_by.length > 25){
            this.deleted_by =  this.deleted_by.substring(0,16) + "..."
        }
    }

    trimName(){
        if (this.name.length > 25){
            this.name =  this.name.substring(0, 25) + "..."
        }
    }

    trimID(){
       this.trimedID = this.id.substring(0, 25) + "..." + this.id.substring(46, 64)
    }

    convertDate(){
        this.date = new Date(this.deleted);
        this.date = (this.date.getDate() + "-" + this.date.getMonth() + "-" + this.date.getFullYear() + " " + 
            this.date.getHours()+":"+this.date.getMinutes()); 
    }

    
}

//sets the page when the document has loaded
window.addEventListener("DOMContentLoaded",()=>{
    deletedPageBrowser = document.querySelector(".browser-deleted-page")
})

//Shows Page(Entry)
function showBrowserDeletedPage(){
    deletedPageBrowser.style.display = "block"

    //check if there is an active search 
    var deleted_file_search_string = document.getElementById("deletedFileSearchInput").value
    if (deleted_file_search_string.length > 0){
        //Search deleted files
        searchDeletedFile()
    }
    else{
        //get deleted files
        getDeletedFiles()
    }
    
}

function hideBrowserDeletedPage(){
    deletedPageBrowser .style.display = "none"
}

// Sets the page loading
function setDeletedFilesLoading(){
    var loadingObject = document.getElementById("deletedFilesLoader")
    if (!loadingObject.classList.contains("show")){
        loadingObject.classList.add("show")
    }
}

// Cancels loading
function cancelDeletedFilesLoading(){
    var loadingObject = document.getElementById("deletedFilesLoader")
    loadingObject.classList.remove("show")
}

//searches deleted file
function searchDeletedFile(){
    if (document.getElementById("deletedFileSearchInput").value == ""){
        getDeletedFiles()
        return
    }

    //Dont do anything if the search string is less than 63
    //This is because file IDs have a length of 64
    if (document.getElementById("deletedFileSearchInput").value.length < 63){
        return
    }
    
    var bodyToShow = document.getElementById("bodyDeletedFiles")

    //data 
    data = {
        "project" : localStorage.getItem("working-project"),
        "criteria" : document.getElementById("deletedFileSearchInput").value
    }

    postToServer("/api/search-deleted-files/", data, function(responce) {
        var deletedObjectArray = JSON.parse(responce)

        //clear body 
        bodyToShow.innerHTML = ""

        //iterate objects
        deletedObjectArray.forEach(element => {
            //new deleted file object
            var newDeletedFile = new deletedFile(element)

            //frame to add to UI
            var frame = `
            <div class="deleted-file-item">
                <div class="categorizer-text hide-mobile">${newDeletedFile.trimedID}</div>
                <div class="categorizer-text">${newDeletedFile.name}</div>
                <div class="categorizer-text hide-mobile ">${newDeletedFile.deleted_by}</div>
                <div class="categorizer-text hide-mobile ">${newDeletedFile.date}</div>
            </div>
            `

            //add to UI
            bodyToShow.innerHTML += frame ;
        });
    })


}

//get deleted files
function getDeletedFiles(){
    //show loading
    set_deleted_files_page_loading(true)

    var bodyToShow = document.getElementById("bodyDeletedFiles")
    //get objects from the server 
    data = {
        "project" : localStorage.getItem("working-project")
    }
    postToServer("/api/get-deleted-files/", data, function(responce) {
        //hide loading 
        set_deleted_files_page_loading(false)
        
        //cancel loading
        cancelDeletedFilesLoading()

        if (responce == "500" || responce == "not found" || responce == "denied"){
            ShowWarning("Fetch Objects Failed")
        }
        else{

            deletedObjectArray = JSON.parse(responce)

            //clear body 
            bodyToShow.innerHTML = ""

            //iterate objects
            deletedObjectArray.forEach(element => {
                //new deleted file object
                var newDeletedFile = new deletedFile(element)

                //frame to add to UI
                var frame = `
                <div class="deleted-file-item">
                    <div class="categorizer-text hide-mobile">${newDeletedFile.trimedID}</div>
                    <div class="categorizer-text">${newDeletedFile.name}</div>
                    <div class="categorizer-text hide-mobile ">${newDeletedFile.deleted_by}</div>
                    <div class="categorizer-text hide-mobile ">${newDeletedFile.date}</div>
                </div>
                `

                //add to UI
                bodyToShow.innerHTML += frame ;
            });
        }
    })

}

//loading 
function set_deleted_files_page_loading(status){
    var loader = document.getElementById("deletedFilesLoader")
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

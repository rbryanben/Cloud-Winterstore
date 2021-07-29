//page
var filesPageBrowser 

//check if loaded 
window.addEventListener("DOMContentLoaded",()=>{
    filesPageBrowser = document.querySelector(".folder-browser-page")
})



//IndexObject Class
// ? Why does it exist
let IndexObject = class {
    constructor(objectID,objectType,objectName,objectSize,objectCreated){
        this.objectID = objectID
        this.objectType = objectType
        this.objectName = objectName
        this.objectSize = objectSize
        this.objectCreated = objectCreated
    }
}

//Directory Object Class 
//This is meant to keep data of a directory
let dirObject = class {
    constructor(folderID,name){
        this.folderID = folderID
        this.folderName = name
    }
}

//Index object selected
//keeps data if an index object is selected. Is used on deciding with modal to show File Modal or Plain Modal
let indexObjectSelected = false

//Focused File
//this keeps data on the selected IndexObject. This can be done because we want to upload or download the file
//and keeps the file data so that there wont be an effect if we ?
let focusedFile ;

/// Showing Folder 
// On opening modals, prevent confusion between the Plain Modal and File Modal.
// Plain  modal checks this before opening
let showingFolder = false

///browser navigation, used to track the current directory
//this array is filled by dirObject objects, that we can pop or push when we move out or into a folder
let browserNavigationMap = [] 

//File Input
//This is an element, so that we can upload files
let fileInputForUpload = document.createElement("input")
let uploadIndex ; //holds the value of the directory to upload the file, because a person may change folders

//Check if initialized
let BrowserPageInitialized = false
let file_browser_initialized_project = null

///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////// Page Show and Hide

//Entry point
function showBrowserFilePage(){
    filesPageBrowser.style.display = "block"
    
    //check if the page was initialized
    if (!BrowserPageInitialized || file_browser_initialized_project != localStorage.getItem("working-project")){
        file_browser_initialized_project = localStorage.getItem("working-project")
        console.log("(File Subpage) initialized for " + file_browser_initialized_project)
        intialize()
    }
}

//hides page
function hideBrowserFilePage(){
    filesPageBrowser.style.display = "none"
}

//function to initialize the page
function intialize(){
    //demonstration
    //check variable and screen
    if (localStorage.getItem("seen-file-browser-demo") && window.innerWidth >= 1000){

        localStorage.removeItem("seen-file-browser-demo")

        //Projects Modal (This should be the only initialization) , Already Initialized
        //initializeDemonstrationModal("demonstationModal")

        //set data
        var client_video_list = []
        client_video_list.push(new DemonstrationObject("/static/video/create_folder.mp4","Create Folder","Lorem ipsum dolor, sit amet consectetur adipisicing elit. Id sapiente dicta assumenda iure porro minus voluptate vitae consectetur laudantium sit iste facere, deleniti, accusantium reprehenderit error neque possimus perferendis debitis?"))
        client_video_list.push(new DemonstrationObject("/static/video/upload_file.mp4","Upload File","Lorem ipsum dolor, sit amet consectetur adipisicing elit. Id sapiente dicta assumenda iure porro minus voluptate vitae consectetur laudantium sit iste facere, deleniti, accusantium reprehenderit error neque possimus perferendis debitis?"))
        client_video_list.push(new DemonstrationObject("/static/video/download_file.mp4","Download File" ,"Lorem ipsum dolor, sit amet consectetur adipisicing elit. Id sapiente dicta assumenda iure porro minus voluptate vitae consectetur laudantium sit iste facere, deleniti, accusantium reprehenderit error neque possimus perferendis debitis?"))
        client_video_list.push(new DemonstrationObject("/static/video/upload_modal.mp4","Open Upload Modal" ,"Lorem ipsum dolor, sit amet consectetur adipisicing elit. Id sapiente dicta assumenda iure porro minus voluptate vitae consectetur laudantium sit iste facere, deleniti, accusantium reprehenderit error neque possimus perferendis debitis?"))
        client_video_list.push(new DemonstrationObject("/static/video/download_modal.mp4","Open Download Modal" ,"Lorem ipsum dolor, sit amet consectetur adipisicing elit. Id sapiente dicta assumenda iure porro minus voluptate vitae consectetur laudantium sit iste facere, deleniti, accusantium reprehenderit error neque possimus perferendis debitis?"))
        client_video_list.push(new DemonstrationObject("/static/video/access_control.mp4","Access Control Modal" ,"Lorem ipsum dolor, sit amet consectetur adipisicing elit. Id sapiente dicta assumenda iure porro minus voluptate vitae consectetur laudantium sit iste facere, deleniti, accusantium reprehenderit error neque possimus perferendis debitis?"))
        client_video_list.push(new DemonstrationObject("/static/video/reload_index.mp4","Reload Index" ,"Lorem ipsum dolor, sit amet consectetur adipisicing elit. Id sapiente dicta assumenda iure porro minus voluptate vitae consectetur laudantium sit iste facere, deleniti, accusantium reprehenderit error neque possimus perferendis debitis?"))

        //show after loading
        setTimeout(()=>{
            loadDemonstrationModal(client_video_list)
        },2000)       
   
    }

    //reset map 
    BrowserPageInitialized = true
    //load files in the root directory 
    loadFiles("root")
}


//browser right column is loading...used when we are trying to retrive something for the right column .i.e files in that 
//directory
function browserPageLoading(){
    if (!document.getElementById("browserLoader").classList.contains("show"))
        document.getElementById("browserLoader").classList.add("show")
}

function browserPageHideLoading(){
    var loader = (document.getElementById("browserLoader"))
    loader.classList.remove("show")
}

///////////////////////////////////////////////////////
///////////////////////////////////////////////////////
/////////////////////////////////////////////////////// Access Control Modal

function updateObjectAccessControl(){
    data = {
        "AUR" : document.getElementById("allowAllUsersReadAccessControl").checked ,
        "AUW" : document.getElementById("allowAllUsersWriteAccessControl").checked,
        "AKW" : document.getElementById("allowKeyUsersWriteAccessControl").checked ,
        "AKR" : document.getElementById("allowKeyUsersReadAccessControl").checked,
        "id" : fileThatHasAccessControlOpen.objectID
    }
    
    putToServer("/api/get-set-access-control/", data, function(responce) {
        if (responce !=  "200"){
            ShowWarning("Connection Error")
        }
    });
}

let fileThatHasAccessControlOpen ;

function showAccessControlModal(){
    var modal = document.getElementById("accessControlModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }
    //loading
    accessControlLoading()

    data = {
        "id" : focusedFile.objectID
    }

    fileThatHasAccessControlOpen = focusedFile

    //set access control  params
    postToServer("/api/get-set-access-control/", data, function(responce) {
        var controls  = JSON.parse(responce)
        document.getElementById("allowAllUsersReadAccessControl").checked = controls['allowAllUsersRead']
        document.getElementById("allowAllUsersWriteAccessControl").checked = controls['allowAllUsersWrite']
        document.getElementById("allowKeyUsersWriteAccessControl").checked = controls['allowKeyUsersWrite']
        document.getElementById("allowKeyUsersReadAccessControl").checked = controls['allowKeyUsersRead']
    });

    //get people with the keys
    postToServer("/api/get-people-with-key/", data, function(responce) {
        hideAccessControlLoading()
        var bodyToPlace = document.getElementById('accounts-with-key')
        bodyToPlace.innerHTML = ""
        JSON.parse(responce).forEach(element => {
            element = `<!-- item frame -->
                    <div class="list-element item">
                        <div class=""><input type="checkbox" class="accountKeyCheckBox" onclick="addSelectedAccountToCheckedList('${element['developerIdentification']}',this)"></div>
                        <div class="categorizer-text">${element['developerIdentification']}</div>
                        <div class="categorizer-text hide-mobile " style="padding-left:8px;"><i class="fas fa-envelope" style="color: gray;"></i></div>
                        <div class="categorizer-text hide-mobile " style="padding-left:11px;">${element['dateObtained']}</div>
                    </div>` 
            bodyToPlace.innerHTML += element
        });

        var listInElement = document.getElementById("accounts-with-key")
        listInElement.style.height = listInElement.clientHeight + "px"
    })
}

function selectAllAccountsWithKeys(object){
    if (object.checked == true){
        var array = document.querySelectorAll(".accountKeyCheckBox")
        array.forEach(element => {
            if (element.checked == false){
                element.click()
            }
        });
    }
    else{
        document.getElementById("deleteAccountKeyButton").classList.remove("show")
        selectedAccountsList = []
        var array = document.querySelectorAll(".accountKeyCheckBox")
        array.forEach(element => {
            if (element.checked == true){
                element.click()
            }
        });
    }
}

function hideAccessControlModal(){
    var modal = document.getElementById("accessControlModal")
    modal.classList.remove("show")
}

function accessControlLoading(){
    var loadingElement = document.getElementById("accessControlLoader")
    if (!loadingElement.classList.contains("show")){
        loadingElement.classList.add("show")
    } 
}

function hideAccessControlLoading(){
    var loadingElement = document.getElementById("accessControlLoader")
    loadingElement.classList.remove("show")
}

function deleteSelectedKeyAccounts(){
    data = {
        "file" : fileThatHasAccessControlOpen.objectID,
        "accounts" : selectedAccountsList
    }

    postToServer("/api/remove-keys/",data, function(responce) {
    if (responce == "200") {
        document.getElementById("deleteAccountKeyButton").classList.remove("show")
        document.getElementById("allKeysSelector").checked = false
        showAccessControlModal()
    } else {
        ShowWarning("Deletion Failed")
    }
    })
}

//access control account selection
let selectedAccountsList = []
function addSelectedAccountToCheckedList(email,object){
    //show delete button
    var deleteButton = document.getElementById("deleteAccountKeyButton")

    if (object.checked == false){
        //remove element 
        removeItemOnce(selectedAccountsList,email)
        //if length is less than 1 then hide bin
        if (selectedAccountsList.length == 0){
            deleteButton.classList.remove("show")
        }

    }
    else {
        selectedAccountsList.push(email)
        if (!deleteButton.classList.contains("show")){
            deleteButton.classList.add("show")
        }
    }
}

function giveKeyToAccountHTTP(){
    //disable button on click to prevent double clicked 
    var give_key_button = document.getElementById("access-control-give-key-button")
    var loading_modal = document.getElementById("give-key-modal-loader")


    data = {
        "account" : document.getElementById("accountKeyIDText").value,
        "file" : (fileThatHasAccessControlOpen.objectID)
    }


    //disable button and show loading
    disableModalButton(give_key_button)
    if (!loading_modal.classList.contains("show")){
        loading_modal.classList.add("show")
    }

    postToServer("/api/give-key/", data, function(responce) {
    //enable button and hide loading 
    enableModalButton(give_key_button)
    loading_modal.classList.remove("show")

    if (responce == "200") {
        hideAddAccountKey()
        showAccessControlModal()
    }
    else if (responce == "not found"){
        ShowWarning("Account Not Found")
    }
    else {
        ShowWarning("Request Failed")
    }
})


}

function showAddAccountKey(){
    var modal = document.getElementById("accountKeyAddModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
        lockUploadAndDownloadModal = true
    }

    //enable button and hide loading 
    var give_key_button = document.getElementById("access-control-give-key-button")
    var loading_modal = document.getElementById("give-key-modal-loader")
    enableModalButton(give_key_button)
    loading_modal.classList.remove("show")
}

function hideAddAccountKey(){
    var modal = document.getElementById("accountKeyAddModal")
    modal.classList.remove("show")
    lockUploadAndDownloadModal = false
}

function removeItemOnce(arr, value) {
    var index = arr.indexOf(value);
    if (index > -1) {
        arr.splice(index, 1);
    }
    return arr;
}

///////////////////////////////////////////////////////
///////////////////////////////////////////////////////
/////////////////////////////////////////////////////// Plain options modal 

//options modal show entry because we need to separate between the file modal
// file modal is for individual files, this one is to create folders, reload index e.t.c , and is different
function showOptionsModal(event){
    if (showingFolder){
        return
    }
    hideOptionsModal()
    showBrowserOptionsModal(event)
}

//plain  options modal
function showBrowserOptionsModal(event){
    var modal = document.getElementById("browserOptionsModal")
    //set  position on mouse position
    modal.style.left = event.clientX + "px"
    modal.style.top = event.clientY + "px"

    //if person clicks on the bottom part of the screen show the options modal on the top of 
    //the cursor , cause options wont be visible at the bottom...same for the x axis
    boundaryPointY = 0.85 * window.innerHeight
    boundaryPointX = 0.82 * window.innerWidth
    if (event.clientY > boundaryPointY){
        modal.style.top = event.clientY - modal.clientHeight + "px"
    }
    if (event.clientX > boundaryPointX){
        modal.style.left = event.clientX - modal.clientWidth+ "px"
    }

    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }
}

//plain options modal hide
function hideBrowserOptionsPage(){
    var modal = document.getElementById("browserOptionsModal")
    modal.classList.remove("show")
}

//new folder option
function plainMenuNewFolderClick(){
    showNameFolderModal()
}

//shows the modal to name a folder once the user clicks "New Folder" in the options modal
function showNameFolderModal(){
    hideRenameModal()
    var modal = document.getElementById("nameFolderModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")    
        lockUploadAndDownloadModal = true
    }
    
}


function hideNameFolderModal(){
    var modal = document.getElementById("nameFolderModal")
    if (modal.classList.contains("show")){
        modal.classList.remove("show")
        lockUploadAndDownloadModal = false
    }
    //hide loading 
    var loading_modal = document.getElementById("name-folder-modal-loader")
    var name_folder_button = document.getElementById("name-folder-button")
    enableModalButton(name_folder_button)
    loading_modal.classList.remove("show")
    
    //clear text in name folder 
    document.getElementById("newFolderName").value = ""
}

//once user has name modal, send the request to the Server 
function createNewFolder(){
    var name = document.getElementById("newFolderName").value
    var parentID = "root"

    if (browserNavigationMap.length > 0){
        parentID = browserNavigationMap[browserNavigationMap.length - 1].folderID
    }
    
    //if folder name is less than 3 alert user
    if (name.length < 3){
        ShowWarning("Check Folder Name")
        return
    }

    data = {
        "folderName" : name,
        "projectName" : localStorage.getItem("working-project"),
        "parentID" : parentID,
    }
    
    //disable button and show request is loading 
    var name_folder_button = document.getElementById("name-folder-button")
    var loading_modal = document.getElementById("name-folder-modal-loader")

    disableModalButton(name_folder_button)
    if (!loading_modal.classList.contains("show")){
        loading_modal.classList.add("show")
    }

    postToServer("/api/new-folder/",data, function(responce) {
        //enable button and show loading
        enableModalButton(name_folder_button)
        loading_modal.classList.remove("show")

        if (responce == "200") {
            hideNameFolderModal()
            reloadFiles()
        }
        else if (responce == "1701"){
            ShowWarning("Repeated Folder Name")
        } 
        else {
            ShowWarning("Folder Creation Failed")
        }
    })

}

///////////////////////////////////////////////////////
///////////////////////////////////////////////////////
/////////////////////////////////////////////////////// File and Folder options modal

//shows options modal after file or folder has been right clicked
function handleRightClick(event,objectID,objectType,objectName,objectSize,objectCreated,object){
    if (selectedObject != object){
        removeAllSelected()
        indexObjectSelected = false
    }
    if (!indexObjectSelected){
        return false
    }
    //showing folder 
    showingFolder = true
    //show options moadal
    var optionsModal = document.getElementById("fileOptionsModal")

    //set  position on mouse position
    optionsModal.style.left = event.clientX + "px"
    optionsModal.style.top = event.clientY + "px"

    //if person clicks on the bottom part of the screen show the options modal on the top of 
    //the cursor , cause options wont be visible at the bottom...same for the x axis
    boundaryPointY = 0.85 * window.innerHeight
    boundaryPointX = 0.82 * window.innerWidth
    if (event.clientY > boundaryPointY){
        optionsModal.style.top = event.clientY - optionsModal.clientHeight + "px"
    }
    if (event.clientX > boundaryPointX){
        optionsModal.style.left = event.clientX - optionsModal.clientWidth+ "px"
    }

    //set new focused file 
    focusedFile = new IndexObject(objectID,objectType,objectName,objectSize,objectCreated)


    //show modal 
    if (!optionsModal.classList.contains("show")){
        hideBrowserOptionsPage()
        optionsModal.classList.add("show")
    }
    return false
}

//hide file options modal
function hideOptionsModal(){
    var optionsModal = document.getElementById("fileOptionsModal")
    optionsModal.classList.remove("show")
    showingFolder = false
}

//open file option 
function menuModalOpenClick(){
//open file or folder through loading the index object 
loadIndexObject(event,focusedFile.objectType,focusedFile.objectID,focusedFile.objectName)
hideOptionsModal()
}

//delete file option
function menuModalDeleteClick(){
    //file to delete json
    data = {
        "id" : focusedFile.objectID
    }
    //delete file via API
    postToServer("/api/delete/", data, function(responce) {
    if (responce == "200") {
        hideOptionsModal()
        reloadFiles()
    } else {
        ShowWarning("Something Went Wrong")
    }
})
}


//show the rename modal 
let objectToRename ;
function showRenameModal(){
    lockUploadAndDownloadModal = true
    hideNameFolderModal()
    var modal = document.getElementById("renameFolderModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }
    //set the textbox to the current filename 
    var renameInput = document.getElementById("renameText")
    renameInput.value =  (focusedFile.objectName)
    renameInput.focus()
    renameInput.select()

    //keep selected file local 
    objectToRename = focusedFile
}

//send rename request 
function sendRenameRequest(){
    //we want to show the loading modal if there is an active http request
    var rename_loading_modal = document.getElementById("rename-modal-loader")
    var rename_modal_button = document.getElementById("renameFolderButton")

    //rename input text
    var renameInput = document.getElementById("renameText")

    //if length of text is less than 3 Notify user
    //else proceed
    if (renameInput.value.length < 3){
        ShowWarning("Check Folder Name")
        return
    }

    //send rename request
    data = {
        "id" : objectToRename.objectID,
        "name" : renameInput.value
    }

    //prevent double click 
    disableModalButton(rename_modal_button)

    //show loading 
    if (!rename_loading_modal.classList.contains("show")){
        rename_loading_modal.classList.add("show")
    }

    postToServer("/api/rename-object/", data, function(responce) {
        if (responce == "200") {
            hideRenameModal()
            reloadFiles()
        } else {
            enableModalButton(rename_modal_button)
            rename_loading_modal.classList.remove("show")
            ShowWarning("Rename Failed")
        }
    })
}

//show the rename modal 
function hideRenameModal(){
    lockUploadAndDownloadModal = false
    var modal = document.getElementById("renameFolderModal")
    modal.classList.remove("show") 

    //enable re-button and hide loading
    //these could have been disabled on request 
    var rename_loading_modal = document.getElementById("rename-modal-loader")
    var rename_modal_button = document.getElementById("renameFolderButton")
    enableModalButton(rename_modal_button)
    rename_loading_modal.classList.remove("show")
}


///////////////////////////////////////////////////////
///////////////////////////////////////////////////////
/////////////////////////////////////////////////////// Functions for files 

//function to load index, this is where files or folders that are clicked are sent
function loadIndexObject(event,objectType,folderRef,folderName){
    if (objectType == "FD"){

        var objectToMap  = new dirObject(folderRef,folderName)
        objectToMap.folderRef = folderRef
        
        //map 
        mapCurrent(objectToMap)
        loadFiles(folderRef)
    }
    else {
        ///if the file download the file 
        var fileRef = folderRef
        var fileName = folderName
        
        ///download file 
        data = {
            "id" : folderRef
        }
        downloadFile(data,fileName)
    }
}

//function to load files for a given folderID, to the files body
function loadFiles(folderID){
    browserPageLoading()
    details = {
        "projectName" : localStorage.getItem("working-project"),
        "folderID" :folderID
    }
    postToServer("/console/get-folder", details, function(responce) {
    if (responce == "500") {
        ShowWarning("Connection Problem")
    } else {
        browserPageHideLoading()
        document.getElementById("browserFilesContent").innerHTML = responce
    }
    })
}

//reload current directory
function reloadFiles(){
    //reload data with the current window
    var currentDirectory;
    if (browserNavigationMap.length > 0){
        currentDirectory = browserNavigationMap[browserNavigationMap.length - 1].folderID
    }
    else {
        currentDirectory = "root"
    }
    loadFiles(currentDirectory)
}

//function to map index given a new dir object 
function mapCurrent(dirObject){
    browserNavigationMap.push(dirObject)
    //add to ui
    if (dirObject.folderName != 'root'){
        var mapPosition = browserNavigationMap.length
        uiElement = `<!--directory --><span class="slash">/</span><span class="directory-name" onclick="goBackward(${mapPosition})" >${dirObject.folderName}</span>`
        document.getElementById("dirMapper").innerHTML += uiElement
    }
}

//function to upload a file, but does not post to serverbut calls the modal to set access control
function uploadFile(){
    fileInputForUpload.type = "file"
    fileInputForUpload.click()
    fileInputForUpload.id = "fileUploads"
    fileInputForUpload.addEventListener("change",function(){
        showUploads()
        document.getElementById("uploadSize").innerHTML = "Size : " + fileInputForUpload.files[0].size
        document.getElementById("uploadName").innerHTML = "Name : " + fileInputForUpload.files[0].name
    })
    //set working index
    if (browserNavigationMap.length == 0){
        uploadIndex = "root"
    }
    else {
        uploadIndex = browserNavigationMap[browserNavigationMap.length - 1].folderID
    }
}

//function to send the file to the server
let request = new XMLHttpRequest();
function sendFile(object){
    //show upload bar 
    var uploadBar = document.getElementById("upload-bar")

    if (object.innerHTML != "Cancel"){
        object.innerHTML = "Cancel"
    }
    else{
        uploadBar.classList.remove("show")
        request.abort()
        object.innerHTML = "Upload"
        return
    }

    try{
        uploadBar.classList.add("show")
        //form data
        var file = fileInputForUpload.files[0];
        var formData = new FormData();
        formData.append("file",file)
        formData.append("name",fileInputForUpload.files[0].name)
        formData.append("size",fileInputForUpload.files[0].size)
        formData.append("project",localStorage.getItem("working-project"))
        //access control 
        formData.append("parent",uploadIndex)
        formData.append("allowAllUsersWrite", document.getElementById("allowAllUsersWrite").checked)
        formData.append("allowAllUsersRead",document.getElementById("allowAllUsersRead").checked)
        formData.append("allowKeyUsersRead",document.getElementById("allowKeyUsersRead").checked)
        formData.append("allowKeyUsersWrite",document.getElementById("allowKeyUsersWrite").checked)

        //show progress bar
        if (!uploadBar.classList.contains("show")){
            uploadBar.classList.add("show")
        }
    
        //xml http 

        request.open('POST', '/console/upload-file'); 
        // upload progress event
        request.onreadystatechange = function() {
        var a;
            if (request.readyState === 4 && request.status === 200) {
                if (request.response == "200"){
                    hideUploads()
                    uploadBar.classList.remove("show")
                    ShowSuccess("Upload Completed")

                    //reload data with the current window
                    reloadFiles()
                }
                else if (request.response == "1702") {
                    ShowWarning("Bad File Name")
                    uploadBar.classList.remove("show")
                }
                else if (request.response == "1703"){
                    ShowWarning("Repeated File Name")
                    uploadBar.classList.remove("show")
                }
            }
        };

        request.upload.addEventListener('progress', function(e) {
            // upload progress as percentage
            let percent_completed = (e.loaded / e.total)*100;
            document.getElementById("upload-progress").style.width = percent_completed +"%";
        });
        // send POST request to server
        request.send(formData);
    }
    catch(err){
        ShowWarning("No File Selected")
    }
}

//goes back to previous directory
function goBackward(n){
    browserNavigationMap = browserNavigationMap.slice(0,n)
    loadFiles(browserNavigationMap[browserNavigationMap.length - 1].folderRef)
    var dirMapper = document.getElementById("dirMapper").innerHTML = ""
    for (var i=0;i != browserNavigationMap.length;i++){
        uiElement = ` <!--directory --><span class="slash">/</span><span class="directory-name" onclick="goBackward(${i + 1})" >${browserNavigationMap[i].folderName}</span>`
        document.getElementById("dirMapper").innerHTML += uiElement
    }
}

//goes to home directory
function goHome(){
    var dirMapper = document.getElementById("dirMapper").innerHTML = " "
    browserNavigationMap = []
    loadFiles('root')
}


function showFilesBin(){
    var bin = document.querySelector(".delete-button-files")
    if (!bin.classList.contains("show")){
        bin.classList.add("show")
    }
}


function hideFilesBin(){
    var bin = document.querySelector(".delete-button-files")
    bin.classList.remove("show")
}


function selectUnselectAllFiles(object){
    if (object.checked){
        array = document.querySelectorAll(".filesCheckboxBox")
        array.forEach(element => {
            if (element.checked == false){
                element.click()
            }
        });
    }
    else {
        array = document.querySelectorAll(".filesCheckboxBox")
        array.forEach(element => {
            if (element.checked){
                element.click()
            }
        });
    }
}

let markedFiles = []
function markFile(id,object){
    if (object.checked){
        markedFiles.push(id)
        showFilesBin()
    }
    else {
        removeItemOnce(markedFiles,id)
        if (markedFiles.length == 0){
            hideFilesBin()
        }
    }
}


function deleteSelectedFiles(){
    markedFiles.forEach(element => {
        data = {
            "id" : element 
        }
        //delete file via API
        postToServer("/api/delete/", data, function(responce) {
        if (responce == "200") {
            hideOptionsModal()
            reloadFiles()
            hideFilesBin()
            document.getElementById("selectUnselectAllFiles").checked = false
        } 
        });
    })
}

//////////////////////////////////////////////////////
//////////////////////////////////////////////////////
////////////////////////////////////////////////////// Global functions

//prevents chrome's properties modal from showing up
window.oncontextmenu= function(){
    return false
}

//for hiding all modals on page click
///seems repeated to me


function removeAllSelected(){
    var AllObjects = document.querySelectorAll(".list-element")
    AllObjects.forEach(element => {
        element.classList.remove("selected")
    });
}

let selectedObject ;
function handleSingleClick(object) { 
    removeAllSelected()
    selectedObject = object
    if (!object.classList.contains("selected")){
        object.classList.add("selected")
    }
    indexObjectSelected = true
}   


function removeAnyModal(){
    hideOptionsModal()
    hideBrowserOptionsPage()
}

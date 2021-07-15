let integrationsSubPageInitialized = false
let activeIntegrationSearch = false
let integrationToDelete = "None"

//initialize
function initializeIntegrationsSubPage(){
    integrationsSubPageInitialized = true
    //get integrations
    getIntegrationsList()
    getPlatformsForIntegrationsHttpRequest()
}

//entry
function showIntegrationsSubPage(){
    //set page visible
    var page = document.getElementById("integrations-subpage")
    page.style.display = "grid"

    //initialize page
    if (integrationsSubPageInitialized == false){
        initializeIntegrationsSubPage()
    }
}


//hide page
    function hideIntegrationsSubPage(){
    //set page visible
    var page = document.getElementById("integrations-subpage")
    page.style.display = "none"
}

//add integrations 
function showAddIntegrationModal(){
    //lock upload and download modal 
    lockUploadAndDownloadModal = true

    var modal = document.getElementById("addIntegrationModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }

    //clear the identification
    document.getElementById("newIntegrationIdentification").value = ""

    //disable button and show loader
    var add_integration_button = document.getElementById("add-integration-modal-button")
    var modal_loader = document.getElementById("add-integration-modal-loader")

    //enable button and hide loader 
    enableModalButton(add_integration_button)
    modal_loader.classList.remove("show")
}

function hideAddIntegrationsModal(){
    lockUploadAndDownloadModal = false
    var modal = document.getElementById("addIntegrationModal")
    modal.classList.remove("show")
}

function addAddIntegrationHttpRequest(){
    var newIntegrationIdentification = document.getElementById("newIntegrationIdentification").value
    var newIntegrationPlatform = document.getElementById("newIntegrationPlatform").value
    var newIntegrationStatus = document.getElementById("newIntegrationStatus").value
    
    //data to update
    data = {
        "identification" : newIntegrationIdentification,
        "platform" : newIntegrationPlatform,
        "status" : newIntegrationStatus,
        "project" : localStorage.getItem("working-project")
    }

    //check if the identification is not empty
    if (newIntegrationIdentification.length < 6){
        ShowWarning("Check Identification")
        return
    }
    
    //disable button and show loader
    var add_integration_button = document.getElementById("add-integration-modal-button")
    var modal_loader = document.getElementById("add-integration-modal-loader")
    disableModalButton(add_integration_button)
    if (!modal_loader.classList.contains("show")){
        modal_loader.classList.add("show")
    }
    //request 
    updateToServer("/console/integrations",data, function(responce) {
        //enable button and hide loader 
        enableModalButton(add_integration_button)
        modal_loader.classList.remove("show")

        if (responce == "200") {
            ShowSuccess("Integration Created")
            hideAddIntegrationsModal()
            if (!activeIntegrationSearch){
                getIntegrationsList()
            }
        } 
        else if(responce == "1705"){
            ShowWarning("Integration Exists")
        }
        else {
            ShowWarning("Something's Wrong")
        }
    })   
}


//get platforms
function getPlatformsForIntegrationsHttpRequest(){
    //body to put set and clear
    var bodyToput = document.getElementById("newIntegrationPlatform")
    var bodyToputUpdateModal = document.getElementById("updateIntegrationPlatform")
    bodyToput.innerHTML = ""
    bodyToputUpdateModal.innerHTML = ""

    getToServer("/console/platforms", null, function(responce) {
        var platformsJSONArray = JSON.parse(responce)

        platformsJSONArray.forEach(platform => {
            frame = `
                <option value="${platform["name"]}">${platform["name"]}</option>
            `
            bodyToput.innerHTML += frame
            bodyToputUpdateModal.innerHTML += frame
        });
    })
}

//get integrations
function getIntegrationsList(){
    setIntegrationsLoading(true)
    //body to display 
    var bodyToDisplay = document.getElementById("bodyIntegrationsList")
    bodyToDisplay.innerHTML = ""

    //data 
    data = {
        "project" : localStorage.getItem("working-project") 
    }

    //request
    postToServer("/console/integrations", data, function(responce) {
        setIntegrationsLoading(false)
        if (responce == "not found" || responce == "Does'nt seem like the JSON we need"){
            ShowWarning("Error Fetching Objects")
        }
        else{
            //array
            IntegrationObjectList = JSON.parse(responce)

            IntegrationObjectList.forEach(jsonObject => {
                var intergrationNew = new Intergration(jsonObject)

                frame = `
                <!-- categorizer -->
                    <div class="integrations-file-item">
                        <div class="categorizer-text ">${intergrationNew.identifier}</div>
                        <div class="categorizer-text hide-mobile ">${jsonObject["platform"]["name"]}</div>
                        <div class="categorizer-text hide-mobile ">${convertDate(jsonObject["created"])}</div>
                        <div class="categorizer-text hide-mobile allow-select ">${jsonObject["integrationKey"]}</div>
                        <div class="categorizer-text controls-client-accounts hide-mobile">
                            <div class="barn-client hide-mobile">
                                <i class="fas fa-sync-alt animate-clicked" onclick="generateNewKeyHttpRequest('${intergrationNew.identifier}',this)"></i>
                            </div>
                            <div class="delete-client hide-mobile">
                                <i class="fas fa-edit" onclick="showUpdateIntegrationsModal('${jsonObject["identifier"]}','${jsonObject["platform"]["name"]}',${jsonObject["enabled"]})"></i>      
                            </div>
                            <div class="edit-client hide-mobile">
                                <i class="fas fa-trash" onclick="showDeleteConfirmationModal('${intergrationNew.identifier}')"></i>
                            </div>
                        </div>  
                    </div>
                    
                `
                bodyToDisplay.innerHTML += frame ;
            });

        }
    })

}

function searchIntegration(object){
    document.getElementById("bodyIntegrationsList").innerHTML = ""
    //if search is empty
    if (object.value.length == 0){
        getIntegrationsList()
        return
    }

    //if search length is 6 or more then search 
    if (object.value.length < 6){
        return
    }

    //start loading
    setIntegrationsLoading(true)

    data = {
        "project" : localStorage.getItem("working-project"),
        "criteria" : object.value
    }

    postToServer("/console/search-update-integrations",data, function(responce) {
        setIntegrationsLoading(false)
        receivedObjects = JSON.parse(responce)
        receivedObjects.forEach(jsonObject => {
            frame = `
                <!-- categorizer -->
                <div class="integrations-file-item">
                    <div class="categorizer-text">${jsonObject["identifier"]}</div>
                    <div class="categorizer-text hide-mobile ">${jsonObject["platform"]["name"]}</div>
                    <div class="categorizer-text hide-mobile ">${convertDate(jsonObject["created"])}</div>
                    <div class="categorizer-text hide-mobile allow-select ">${jsonObject["integrationKey"]}</div>
                
                    <div class="categorizer-text controls-client-accounts hide-mobile">
                        <div class="barn-client hide-mobile">
                            <i class="fas fa-sync-alt animate-clicked" onclick="generateNewKeyHttpRequest('${jsonObject["identifier"]}',this)"></i>
                        </div>
                        <div class="delete-client hide-mobile">
                            <i class="fas fa-edit" onclick="showUpdateIntegrationsModal('${jsonObject["identifier"]}','${jsonObject["platform"]["name"]}',${jsonObject["enabled"]})"></i>          
                        </div>
                        <div class="edit-client hide-mobile">
                            <i class="fas fa-trash" onclick="showDeleteConfirmationModal('${jsonObject["identifier"]}')"></i>
                        </div>
                    </div>  
                </div> 
            `

            document.getElementById("bodyIntegrationsList").innerHTML += frame
        });
    })
}

//loading
function setIntegrationsLoading(stateLoading){
    var loadingModal = document.getElementById("integrationsLoadingModal")
    if (stateLoading == false){
        loadingModal.classList.remove("show")
    }
    else if (stateLoading == true){
        if (!loadingModal.classList.contains("show")){
            loadingModal.classList.add("show")
        }
    }
}

//generate new key
function generateNewKeyHttpRequest(integration,object){
    //animate
    if (!object.classList.contains("animate")){
        object.classList.add("animate")
    }
    
    data = {
        "identification" : integration,
        "project" : localStorage.getItem("working-project")
    }

    postToServer("/console/generate-new-key", data, function(responce) {
        if (responce == "200") {
            ShowSuccess("Key Generated")
            if (!activeIntegrationSearch){
                getIntegrationsList()
            }
        } else {
            ShowWarning("Server Error")
        }
    })
}

//update integration
let integrationToUpdate = "None"

function showUpdateIntegrationsModal(identification,platform,status){
    //lock upload and download modal
    lockUploadAndDownloadModal = true

    var modal = document.getElementById("updateIntegrationModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }

    //elements
    var updateIntegrationsInput= document.getElementById("updateIntegrationIdentification")
    var updateIntegrationsStatus = document.getElementById("updateIntegrationStatus")
    var updateIntegrationPlatform = document.getElementById("updateIntegrationPlatform")

    updateIntegrationsInput.value = identification
    integrationToUpdate = identification
    //set status
    if (status){
        updateIntegrationsStatus.value = "Active"
    }
    else {
        updateIntegrationsStatus.value = "Disabled"
    }

    //set platform
    updateIntegrationPlatform.value = platform

    //enable button and hide loading 
    var update_modal_button = document.getElementById("update-integration-modal-button")
    var modal_loader = document.getElementById("update-integration-modal-loader")
    //enable button and hide loading
    enableModalButton(update_modal_button)
    modal_loader.classList.remove("show")
}

//update integration httprequest
function updateIntegrationHttpRequest(){
    //elements
    var updateIntegrationsInput= document.getElementById("updateIntegrationIdentification")
    var updateIntegrationsStatus = document.getElementById("updateIntegrationStatus")
    var updateIntegrationPlatform = document.getElementById("updateIntegrationPlatform")

    //check the length of the identification 
    if (updateIntegrationsInput.value.length < 6){
        ShowWarning("Check Identification")
        return
    }

    //disable button and show loading 
    var update_modal_button = document.getElementById("update-integration-modal-button")
    var modal_loader = document.getElementById("update-integration-modal-loader")
    disableModalButton(update_modal_button)
    if (!modal_loader.classList.contains("show")){
        modal_loader.classList.add("show")
    }

    data = {
        "project" : localStorage.getItem("working-project"),
        "platform" : updateIntegrationPlatform.value,
        "identification" : updateIntegrationsInput.value,
        "status" : updateIntegrationsStatus.value,
        "id" : integrationToUpdate
    }

    //request
    patchToServer("/console/integrations", data, function(responce) {
        //enable button and hide loading
        enableModalButton(update_modal_button)
        modal_loader.classList.remove("show")

        if (responce == "200"){
            if (!activeIntegrationSearch){
                hideUpdateIntegrationsModal()
                getIntegrationsList()
            }
            ShowSuccess("Integration Updated")
        }
    })
}

function hideUpdateIntegrationsModal(){
    //unlock upload and download modal 
    lockUploadAndDownloadModal = false
    
    var modal = document.getElementById("updateIntegrationModal")
    modal.classList.remove("show")
}

//Delete Integration
function showDeleteConfirmationModal(identification){
    var modal = document.getElementById("deleteIntegrationModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }
    //set the integration
    integrationToDelete = identification
    document.getElementById("deleteIntegrationIdentification").value = identification

    //enable Button and Show Loading 
    var delete_integration_button = document.getElementById("delete-integration-button")
    var modal_loader = document.getElementById("delete-integration-modal-loader")
    enableModalButton(delete_integration_button)
    modal_loader.classList.remove("show")
}

function hideDeleteIntegrationModal(){
    var modal = document.getElementById("deleteIntegrationModal")
    modal.classList.remove("show")
}

function deleteIntegrationHttpRequest(){
    data = {
        "identification" : integrationToDelete,
        "project" : localStorage.getItem("working-project")
    }

    //Disable Button and Show Loading 
    var delete_integration_button = document.getElementById("delete-integration-button")
    var modal_loader = document.getElementById("delete-integration-modal-loader")
    disableModalButton(delete_integration_button)
    if (!modal_loader.classList.contains("show")){
        modal_loader.classList.add("show")
    }

    deleteToServer("/console/integrations", data, function(responce) {
        //enable button and hide loading
        enableModalButton(delete_integration_button)
        modal_loader.classList.remove("show")
        if (responce == "200") {
            ShowSuccess("Integration Deleted")
            document.getElementById("integrationsSearchInput").value = ""
            getIntegrationsList()
            hideDeleteIntegrationModal()
        } else {
            ShowWarning("Deletion Error")
        }
    })
}


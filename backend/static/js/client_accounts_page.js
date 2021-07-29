let activeClientSearch = false

//integration class 
let Intergration = class {
    
    constructor(jsonObject){
        this.identifier = jsonObject["identifier"]
        this.enabled = jsonObject["enabled"]  
        this.created = ["created"]  
        this.integrationKey = ["integrationKey"] 
        this.platform = ["platform"]["name"] 
    }

}

//developer client class
let DeveloperClient = class{
    constructor(developerClient){
        this.user = developerClient["user"]
        this.identification =  developerClient["identification"]
        this.date_joined =  developerClient["user"]["date_joined"]
        this.last_login =  developerClient["last_login"]
        this.token =  developerClient["token"]
        this.date_joined = convertDate(this.date_joined)
        this.last_login = convertDate(this.last_login)
        this.isBarned = developerClient["isBarned"]
        this.integration = developerClient["integration"]["identifier"]
    }
}

//get clients
function getDeveloperClients(){
    ClientPageShowLoading()

    //body to display
    bodyToDisplay = document.getElementById("clients-accounts-list")
    bodyToDisplay.innerHTML = ""

    data = {
        "project" : localStorage.getItem("working-project")
    }

    //requests
    postToServer("/console/developer-clients", data, function(responce) {
        ClientPageCancelLoading()
        if (responce == "not found" || responce == "Does'nt seem like the JSON we need"){
            ShowWarning("Error Fetching Objects")
        }
        else {
            //array
            developerClientsArray = JSON.parse(responce)

            developerClientsArray.forEach(developerClient => {
                var developerClientNew = new DeveloperClient(developerClient)
                
                //frame unbarned
                frameUnbanned = `
                    <div class="client-item">
                        <div class="categorizer-text">${developerClientNew.identification}</div>
                        <div class="categorizer-text hide-mobile ">${developerClientNew.date_joined}</div>
                        <div class="categorizer-text hide-mobile ">${developerClientNew.last_login}</div>
                        <div class="categorizer-text hide-mobile allow-select ">${developerClientNew.token}</div>
                        <div class="categorizer-text controls-client-accounts hide-mobile">
                                <div class="barn-client hide-mobile">
                                    <i class="fas fa-ban" onclick="showBarnAccountModal('${developerClientNew.identification}')"></i>
                                </div>
                                <div class="delete-client hide-mobile">
                                    <i class="fas fa-edit" onclick="showEditClientModal('${developerClientNew.identification}','${developerClientNew.integration}')"></i>          
                                </div>
                                <div class="edit-client hide-mobile">
                                    <i class="fas fa-trash" onclick="showDeleteAccountModal('${developerClientNew.identification}','${developerClientNew.integration}')"></i>
                                </div>
                            </div>
                        </div>
                `
        
                //frame barned
                frameBanned = `
                    <div class="client-item barned">
                        <div class="categorizer-text">${developerClientNew.identification}</div>
                        <div class="categorizer-text hide-mobile ">${developerClientNew.date_joined}</div>
                        <div class="categorizer-text hide-mobile ">${developerClientNew.last_login}</div>
                        <div class="categorizer-text hide-mobile allow-select ">${developerClientNew.token}</div>
                        <div class="categorizer-text controls-client-accounts hide-mobile">
                                <div class="barn-client hide-mobile">
                                    <i class="fas fa-ban" onclick="showRemoveBarnModal('${developerClientNew.identification}')"></i>
                                </div>
                                <div class="delete-client hide-mobile">
                                    <i class="fas fa-edit" onclick="showEditClientModal('${developerClientNew.identification}','${developerClientNew.integration}')"></i>         
                                </div>
                                <div class="edit-client hide-mobile">
                                    <i class="fas fa-trash" onclick="showDeleteAccountModal('${developerClientNew.identification}','${developerClientNew.integration}')"></i>
                                </div>
                            </div>
                        </div>
                `

                if (developerClientNew.isBarned){
                    bodyToDisplay.innerHTML += frameBanned
                }
                else{
                    bodyToDisplay.innerHTML += frameUnbanned
                }
                
            });
            
        }
    })

}

//delete account
let clientAccountToDeleteIntegration = 'none'
function showDeleteAccountModal(identification,integration){
    var modal = document.getElementById("deleteClientAccountModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }
    var identificationInput = document.getElementById("deleteClientAccountIdentification")
    identificationInput.value =  identification
    clientAccountToDeleteIntegration = integration

    //enable button and hide loading
    var delete_client_button = document.getElementById("delete-client-account-modal-button")
    var modal_loader = document.getElementById("delete-client-account-modal-loader")

    //enable button and hide loading
    enableModalButton(delete_client_button)
    modal_loader.classList.remove("show")
}


function hideDeleteAccountModal(){
    var modal = document.getElementById("deleteClientAccountModal")
    modal.classList.remove("show")
}

function deleteClientAccountHttpRequest(){
    data = {
        "integration" : clientAccountToDeleteIntegration,
        "password" : "none",
        "project" : localStorage.getItem("working-project"),
        "identification" : document.getElementById("deleteClientAccountIdentification").value
    }

    //disable button and show loading
    var delete_client_button = document.getElementById("delete-client-account-modal-button")
    var modal_loader = document.getElementById("delete-client-account-modal-loader")

    disableModalButton(delete_client_button)
    if (!modal_loader.classList.contains("show")){
        modal_loader.classList.add("show")
    }

    //delete the account
    deleteToServer("/console/add-developer-client", data, function(responce) {
        //enable button and hide loading
        enableModalButton(delete_client_button)
        modal_loader.classList.remove("show")

        if (responce == "200") {
            ShowSuccess("Client Account Deleted")
            hideDeleteAccountModal()
            if (!activeClientSearch){
                getDeveloperClients()
                return
            }
            searchClientAccounts(document.getElementById("searchClientInput"))
        } 
        else if (responce == "1704"){
            ShowWarning("Client Doesn't Exists")
        }
        else {
            ShowWarning("Error Deleting Account")
        }
    })
}

// edit or update client modal
function showEditClientModal(identification, integrationClient){
    //add upload and download lock  
    lockUploadAndDownloadModal = true

    var modal = document.getElementById("editClientAccountModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }

    //set identification
    document.getElementById("updateClientAccountIdentifierInput").value = identification
    //set integration 
    
    document.getElementById("updateClientIntegrations").value = integrationClient

    //disble button and show loading
    var edit_client_button = document.getElementById("edit-client-account-modal-button")
    var modal_loader = document.getElementById("edit-client-account-modal-loader")

    //enable button
    enableModalButton(edit_client_button)
    modal_loader.classList.remove("show")
}

function hideEditClientModal(){
    //release upload and download lock  
    lockUploadAndDownloadModal = false

    var modal = document.getElementById("editClientAccountModal")
    modal.classList.remove("show")
}

function updateClientHttpRequest(){

    //check integration existance
    if (document.getElementById("updateClientIntegrations").value == ""){
        ShowWarning("No Integration Selected")
        return
    }

    //check username length 
    if (document.getElementById("updateClientAccountIdentifierInput").value.length < 6){
        ShowWarning("Identification Too Short")
        return
    }

    //check password
    if (document.getElementById("updateClientAccountPassword").value.length < 6){
        ShowWarning("Password Too Short")
        return
    }

    data = {
        "integration" : document.getElementById("updateClientIntegrations").value,
        "password" : document.getElementById("updateClientAccountPassword").value,
        "project" : localStorage.getItem("working-project"),
        "identification" : document.getElementById("updateClientAccountIdentifierInput").value
    }

    //disble button and show loading
    var edit_client_button = document.getElementById("edit-client-account-modal-button")
    var modal_loader = document.getElementById("edit-client-account-modal-loader")
    disableModalButton(edit_client_button)
    if (!modal_loader.classList.contains("show")){
        modal_loader.classList.add("show")
    }

    //create the account
    updateToServer("/console/add-developer-client", data, function(responce) {
        //enable button and hide loading
        enableModalButton(edit_client_button)
        modal_loader.classList.remove("show")

        if (responce == "200") {
            ShowSuccess("Client Account Updated")
            hideEditClientModal()
            if (!activeClientSearch){
                getDeveloperClients()
                return
            }     
            searchClientAccounts(document.getElementById("searchClientInput"))
        } 
        else if (responce == "1704"){
            ShowWarning("Client Does'nt Exists")
        }
        else {
            ShowWarning("Error Creating Account")
        }
    })
}

//client accounts
function showClientAccounts(){
    //demonstration
    //check variable and screen
    if (localStorage.getItem("seen-accounts-page-demo") && window.innerWidth >= 1000){

        localStorage.removeItem("seen-accounts-page-demo")

        //Projects Modal (This should be the only initialization) , Already Initialized
        //initializeDemonstrationModal("demonstationModal")

        //set data
        var client_accounts_video_list = []
        client_accounts_video_list.push(new DemonstrationObject("/static/video/client_account_create.mp4","Create Account","Create a Client Account by simply clicking the add button on the top right corner. A modal will be show to which you will define the Integration to add the account to, the identification of the client and their password."))
        client_accounts_video_list.push(new DemonstrationObject("/static/video/barn.mp4","Barn Account","Barn a Client Account by clicking the Barn button. Barning a client will prevent them from uploading and downloading files to and from the project. Barning takes imediate effect."))
        client_accounts_video_list.push(new DemonstrationObject("/static/video/unbarn.mp4","Remove Barn" ,"Remove Barn for Client Account by clicking the Barn button again. Removing Barn means client will be able to upload and download a files to and from the project.Removing Barn takes imediate effect."))
       
        //show after loading
        setTimeout(()=>{
            loadDemonstrationModal(client_accounts_video_list)
        },500)       
   
    }

    //page
    var pageClientAccounts = document.getElementById("client-accounts")

    //show
    pageClientAccounts.style.display = "grid"

    //get integrations
    getIntegrations()
    getDeveloperClients()
}

function hideClientAccounts(){
    //page
    var pageClientAccounts = document.getElementById("client-accounts")

    //show
    pageClientAccounts.style.display = "none"
}

//barn client account
function showBarnAccountModal(identifier){
    var modal = document.getElementById("barnClientAccountModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }

    var accountToBarnIdentificationSpan = document.getElementById("accountToBarnIdentificationSpan")
    accountToBarnIdentificationSpan.value = identifier

    //enable button and hide loading
    var barn_client_button = document.getElementById("barn-client-account-modal-button")
    var modal_loader = document.getElementById("barn-client-account-modal-loader")

    enableModalButton(barn_client_button)
    modal_loader.classList.remove("show")
}

function hideBarnAccountModal(){
    var modal = document.getElementById("barnClientAccountModal")
    modal.classList.remove("show")
}

function barnClientAccountHttpRequest(){
    //disable button and show loading
    var barn_client_button = document.getElementById("barn-client-account-modal-button")
    var modal_loader = document.getElementById("barn-client-account-modal-loader")
    //disable button and show loading
    disableModalButton(barn_client_button)
    if (!modal_loader.classList.contains("show")){
        modal_loader.classList.add("show")
    }

    account_to_barn = {
        "identification" : document.getElementById("accountToBarnIdentificationSpan").value,
        "project" : localStorage.getItem("working-project")
    }

    postToServer("/console/barn-client-account", account_to_barn, function(responce) {
        //enable button after receiving an http response 
        enableModalButton(barn_client_button)
        modal_loader.classList.remove("show")

        if (responce == "500" || responce == "not found") {
            ShowWarning("Client Not Found")
        } else {
            ShowSuccess("Ban Successful")
            hideBarnAccountModal()
            if (activeClientSearch){
                searchClientAccounts(document.getElementById("searchClientInput"))
                return
            }
            getDeveloperClients()
        }
    })
}

//remove barn 
function showRemoveBarnModal(identification){
    var modal = document.getElementById("removeBarnClientAccountModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }

    //set the identification
    document.getElementById("accountToRemoveBarnIdentificationInput").value = identification

    //enable barn button and hide loading
    var remove_barn_button = document.getElementById("remove-barn-button")
    var modal_loader = document.getElementById("remove-barn-loader")

    //enable button and hide loading
    enableModalButton(remove_barn_button)
    modal_loader.classList.remove("show")
}

function hideRemoveBarnAccountModal(){
    var modal = document.getElementById("removeBarnClientAccountModal")
    modal.classList.remove("show")
}

function removeBarnClientAccountHttpRequest(){
    //disable button and show loading 
    var remove_barn_button = document.getElementById("remove-barn-button")
    var modal_loader = document.getElementById("remove-barn-loader")
    disableModalButton(remove_barn_button)
    if (!modal_loader.classList.contains("show")){
        modal_loader.classList.add("show")
    }

    account_to_remove_barn = {
        "identification" : document.getElementById("accountToRemoveBarnIdentificationInput").value,
        "project" : localStorage.getItem("working-project")
    }

    postToServer("/console/remove-barn-client-account", account_to_remove_barn, function(responce) {
        //enable button after receiving responce from server
        enableModalButton(remove_barn_button)
        modal_loader.classList.remove("show")

        if (responce == "500" || responce == "not found") {
            ShowWarning("Client Not Found")
        } else {
            ShowSuccess("Ban Removed")
            hideRemoveBarnAccountModal()
            if (activeClientSearch){
                searchClientAccounts(document.getElementById("searchClientInput"))
                return
            }
            getDeveloperClients()
        }
    })
}

//loading page 
function ClientPageShowLoading(){
    var modal = document.getElementById("clientAccountPageLoader")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }
}

function ClientPageCancelLoading(){
    var modal = document.getElementById("clientAccountPageLoader")
    modal.classList.remove("show")
}

//search client account 
function searchClientAccounts(object){
    if (object.value == ""){
        activeClientSearch = false
        getDeveloperClients()
    }
    else {
        activeClientSearch =true
        //search data
        ClientPageShowLoading()

    //body to display
        bodyToDisplay = document.getElementById("clients-accounts-list")
        bodyToDisplay.innerHTML = ""

        data = {
            "project" : localStorage.getItem("working-project"),
            'criteria' : object.value
        }

        //requests
        postToServer("/console/search-developer-clients", data, function(responce) {
            ClientPageCancelLoading()
        
            //array
            developerClientsArray = JSON.parse(responce)

            developerClientsArray.forEach(developerClient => {
                var developerClientNew = new DeveloperClient(developerClient)
                
                    //frame unbarned
                frameUnbanned = `
                    <div class="client-item">
                        <div class="categorizer-text">${developerClientNew.identification}</div>
                        <div class="categorizer-text hide-mobile ">${developerClientNew.date_joined}</div>
                        <div class="categorizer-text hide-mobile ">${developerClientNew.last_login}</div>
                        <div class="categorizer-text hide-mobile allow-select ">${developerClientNew.token}</div>
                        <div class="categorizer-text controls-client-accounts hide-mobile">
                                <div class="barn-client hide-mobile">
                                    <i class="fas fa-ban" onclick="showBarnAccountModal('${developerClientNew.identification}')"></i>
                                </div>
                                <div class="delete-client hide-mobile">
                                    <i class="fas fa-edit" onclick="showEditClientModal('${developerClientNew.identification}','${developerClientNew.integration}')"></i>          
                                </div>
                                <div class="edit-client hide-mobile">
                                    <i class="fas fa-trash" onclick="showDeleteAccountModal('${developerClientNew.identification}','${developerClientNew.integration}')"></i>
                                </div>
                            </div>
                        </div>
                `
        
                //frame barned
                frameBanned = `
                    <div class="client-item barned">
                        <div class="categorizer-text">${developerClientNew.identification}</div>
                        <div class="categorizer-text hide-mobile ">${developerClientNew.date_joined}</div>
                        <div class="categorizer-text hide-mobile ">${developerClientNew.last_login}</div>
                        <div class="categorizer-text hide-mobile allow-select ">${developerClientNew.token}</div>
                        <div class="categorizer-text controls-client-accounts hide-mobile">
                                <div class="barn-client hide-mobile">
                                    <i class="fas fa-ban" onclick="showRemoveBarnModal('${developerClientNew.identification}')"></i>
                                </div>
                                <div class="delete-client hide-mobile">
                                    <i class="fas fa-edit" onclick="showEditClientModal('${developerClientNew.identification}','${developerClientNew.integration}')"></i>         
                                </div>
                                <div class="edit-client hide-mobile">
                                    <i class="fas fa-trash" onclick="showDeleteAccountModal('${developerClientNew.identification}','${developerClientNew.integration}')"></i>
                                </div>
                            </div>
                        </div>
                `
                if (developerClientNew.isBarned){
                    bodyToDisplay.innerHTML += frameBanned
                }
                else{
                    bodyToDisplay.innerHTML += frameUnbanned
                }
                
            });
        
        })

    }

}

//add client account
function getIntegrations(){
    //body to display 
    var bodyToDisplay = document.getElementById("addClientIntegrations")
    bodyToDisplay.innerHTML = ""

    //data 
    data = {
        "project" : localStorage.getItem("working-project") 
    }

    //request
    postToServer("/console/integrations", data, function(responce) {
        if (responce == "not found" || responce == "Does'nt seem like the JSON we need"){
            ShowWarning("Error Fetching Objects")
        }
        else{
            //array
            IntegrationObjectList = JSON.parse(responce)

            IntegrationObjectList.forEach(jsonObject => {
                intergration = new Intergration(jsonObject)
                frame = `
                    <option value="${intergration.identifier}">${intergration.identifier}</option>
                `
                bodyToDisplay.innerHTML += frame ;
            });

        }
    })

}

function showAddClientModal(){
    //lock upload and download modal 
    lockUploadAndDownloadModal = true

    var modal = document.getElementById("addClientAccount")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }

    document.getElementById("newClientAccountIdentification").value = ""
    document.getElementById("newClientPasswordinput").value = ""

    //enable button and show loading
    var add_client_button = document.getElementById("add-client-account-modal-button")
    var modal_loader = document.getElementById("add-client-account-modal-loader")

    //enable button when fetch is complete
    enableModalButton(add_client_button)
    modal_loader.classList.remove("show")
}

function hideAddClientModal(){
    //release upload and download lock  
    lockUploadAndDownloadModal = false

    var modal = document.getElementById("addClientAccount")
    modal.classList.remove("show")
}

function addClientAccount(){

    //check integration existance
    if (document.getElementById("addClientIntegrations").value == ""){
        ShowWarning("No Integration Selected")
        return
    }

    //check username length 
    if (document.getElementById("newClientAccountIdentification").value.length < 6){
        ShowWarning("Identification Too Short")
        return
    }

    //check password
    if (document.getElementById("newClientPasswordinput").value.length < 6){
        ShowWarning("Password Too Short")
        return
    }

    data = {
        "integration" : document.getElementById("addClientIntegrations").value,
        "password" : document.getElementById("newClientPasswordinput").value,
        "project" : localStorage.getItem("working-project"),
        "identification" : document.getElementById("newClientAccountIdentification").value
    }

    //disable button and show loading
    var add_client_button = document.getElementById("add-client-account-modal-button")
    var modal_loader = document.getElementById("add-client-account-modal-loader")
    disableModalButton(add_client_button)
    if (!modal_loader.classList.contains("show")){
        modal_loader.classList.add("show")
    }

    //create the account
    postToServer("/console/add-developer-client", data, function(responce) {
        //enable button when fetch is complete
        enableModalButton(add_client_button)
        modal_loader.classList.remove("show")

        if (responce == "200") {
            ShowSuccess("Client Account Created")
            hideAddClientModal()
            getDeveloperClients()
        } 
        else if (responce == "1704"){
            ShowWarning("Client Account Exists")
        }
        else {
            ShowWarning("Error Creating Account")
        }
    })

}

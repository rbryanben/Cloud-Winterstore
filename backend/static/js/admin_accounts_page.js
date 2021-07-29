let adminAccountsPageInitilized =false
let activeAdminAccountSearch = false

let AdminAccountClass = class {
    constructor(JSONObject){
        this.identification =  JSONObject["identification"]
        this.last_login = convertDate(JSONObject["last_login"])
        this.added = convertDate(JSONObject["added"])
    }
}

//loading 
function adminAccountPageLoading(){
    var loading = document.getElementById("adminAccountPageLoader")
    if (!loading.classList.contains("show")){
        loading.classList.add("show")
    }
}

function adminAccountPageLoadingCancel(){
    var loading = document.getElementById("adminAccountPageLoader")
    if (loading.classList.contains("show")){
        loading.classList.remove("show")
    }
}

//add admin account 
function showAddAdminAccountModal(){
    //add upload and download lock  
    lockUploadAndDownloadModal = true

    var modal = document.getElementById("addAdminAccountModal")
    document.getElementById('newAdminAccountIdentification').value = ""
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }

    //enable button and hide loading 
    var add_admin_account = document.getElementById("add-admin-account-modal-button")
    var modal_loader = document.getElementById("add-admin-account-modal-loader")

    //enable button and hide loading after receiving response fromserver 
    enableModalButton(add_admin_account)
    modal_loader.classList.remove("show")
}

function hideAddAdminAccountModal(){
    //release upload and download lock  
    lockUploadAndDownloadModal = false

    var modal = document.getElementById("addAdminAccountModal")
    if (modal.classList.contains("show")){
        modal.classList.remove("show")
    }
}

function addAdminAccountHttpRequest(){
    data = {
        "project" : localStorage.getItem("working-project"),
        "identification" : document.getElementById("newAdminAccountIdentification").value
    }

    //check length 
    if (data["identification"].length < 6){
        ShowWarning("Invalid Email")
        return
    }
    
    //disable button and show loading 
    var add_admin_account = document.getElementById("add-admin-account-modal-button")
    var modal_loader = document.getElementById("add-admin-account-modal-loader")
    
    disableModalButton(add_admin_account)
    if (!modal_loader.classList.contains("show")){
        modal_loader.classList.add("show")
    }

    putToServer("/console/project-admin-clients", data, function(responce) {
        //enable button and hide loading after receiving response fromserver 
        enableModalButton(add_admin_account)
        modal_loader.classList.remove("show")

        if (responce == "200") {
            ShowSuccess("Account Added")
            hideAddAdminAccountModal()
            if (!activeAdminAccountSearch){
                getAdminAccounts()
            }
        } else {
            ShowWarning("Request Failed")
        }
    })

}

//show delete confirmation 
function showDeleteAdminAccountModal(identification){
    var modal = document.getElementById("deleteAdminAccountModal")
    if (!modal.classList.contains("show")){
        modal.classList.add("show")
    }

    document.getElementById("deleteAdminAccountIdentification").value = identification

    //enable button and hide loading
    var delete_admin_button = document.getElementById("delete-admin-account-modal-button")
    var modal_loader = document.getElementById("delete-admin-account-modal-loader")
    enableModalButton(delete_admin_button)
    modal_loader.classList.remove("show")
}

function hideDeleteAdminModal(){
    var modal = document.getElementById("deleteAdminAccountModal")
    if (modal.classList.contains("show")){
        modal.classList.remove("show")
    }
}

function deleteAdminAccountHttpRequest(){
    //disable button and show loading 
    var delete_admin_button = document.getElementById("delete-admin-account-modal-button")
    var modal_loader = document.getElementById("delete-admin-account-modal-loader")

    disableModalButton(delete_admin_button)
    if (!modal_loader.classList.contains("show")){
        modal_loader.classList.add("show")
    }

    data = {
        "project" : localStorage.getItem("working-project"),
        "identification" : document.getElementById("deleteAdminAccountIdentification").value
    }

    deleteToServer("/console/project-admin-clients", data, function(responce) {
        //enable button after receiving response 
        enableModalButton(delete_admin_button)
        modal_loader.classList.remove("show")

        if (responce == "200") {
            if (activeAdminAccountSearch == false){
                hideDeleteAdminModal()
                ShowSuccess("Deleted Account")
                getAdminAccounts()
            }
            else {
                document.getElementById("searchadminInput").value == ""
                ShowSuccess("Deleted Account")
                hideDeleteAdminModal()
            }
        } else {
            ShowWarning("Delete Account Failed")
        }
    })
}

//page show and hide
function showAdminAccounts(){
    //page
    var pageAdminAccounts = document.getElementById("admin-accounts-accounts")

    //show
    pageAdminAccounts.style.display = "grid"

    //initialize
    initializeAdminAccountsPage()
}

function hideAdminAccounts(){
    //page
    var pageAdminAccounts = document.getElementById("admin-accounts-accounts")

    //show
    pageAdminAccounts.style.display = "none"
}

function initializeAdminAccountsPage(){
    getAdminAccounts();

    //demonstration
    //check variable and screen
    //hide demonstration modal 
    demonstationModalSetShow(false)
    if (localStorage.getItem("seen-admin-accounts-page-demo") && window.innerWidth >= 1000){

        localStorage.removeItem("seen-admin-accounts-page-demo")
        //Projects Modal (This should be the only initialization) , Already Initialized
        //initializeDemonstrationModal("demonstationModal")

        //set data
        var client_accounts_video_list = []
        client_accounts_video_list.push(new DemonstrationObject("/static/video/add_someone.mp4","Add Someone","Add someone else to manage this project by click the add button, and then define the identification for the person to add. Identification takes the form of an email and rather not the username of the person. Upon adding the project will appear on the person's console."))
 
        //show after loading
        setTimeout(()=>{
            loadDemonstrationModal(client_accounts_video_list)
        },500)       
   
    }
}


//get admin accounts
function getAdminAccounts(){
    adminAccountPageLoading()
    var bodyToAdd = document.getElementById("admins-accounts-list")
    bodyToAdd.innerHTML = ""
    data = {
        "project" : localStorage.getItem("working-project")
    }

    postToServer("/console/project-admin-clients", data, function(responce) {
        adminAccountPageLoadingCancel()
        if (responce == "500") {
            ShowWarning("Error Fetching Objects")
        } else {  
            var receivedAdminAccounts = JSON.parse(responce)
            //iterate 
            receivedAdminAccounts.forEach(JSONObject => {
                //add to object
                var newAdminAccount = new AdminAccountClass(JSONObject)
                //frame 
                var frame = `
                    <div class="admin-item">
                        <div class="categorizer-text ">${newAdminAccount.identification}</div>
                        <div class="categorizer-text hide-mobile ">${newAdminAccount.added}</div>
                        <div class="categorizer-text hide-mobile ">${newAdminAccount.last_login}</div>
                        <div class="categorizer-text hide-mobile">
                            <!-- Bin-->
                            <div style="margin-left: 20px;">
                                <i class="fas fa-trash" onclick="showDeleteAdminAccountModal('${newAdminAccount.identification}')"></i>  
                            </div>  
                        </div>
                    </div>
                `

                bodyToAdd.innerHTML += frame
            });
        }
    })

}

//search admin account
function searchAdminAccount(){
    adminAccountPageLoading()
    if (document.getElementById("searchadminInput").value == ""){
        getAdminAccounts()
        activeAdminAccountSearch = false
        return
    }
    activeAdminAccountSearch = true
    var bodyToAdd = document.getElementById("admins-accounts-list")
    bodyToAdd.innerHTML = ""
    data = {
        "project" : localStorage.getItem("working-project"),
        "identification" : document.getElementById("searchadminInput").value
    }

    patchToServer("/console/project-admin-clients", data, function(responce) {
        adminAccountPageLoadingCancel()
        if (responce == "500") {
            ShowWarning("Error Fetching Objects")
        } else {  
            var receivedAdminAccounts = JSON.parse(responce)
            //iterate 
            receivedAdminAccounts.forEach(JSONObject => {
                //add to object
                var newAdminAccount = new AdminAccountClass(JSONObject)
                //frame 
                var frame = `
                    <div class="admin-item">
                        <div class="categorizer-text ">${newAdminAccount.identification}</div>
                        <div class="categorizer-text hide-mobile ">${newAdminAccount.added}</div>
                        <div class="categorizer-text hide-mobile ">${newAdminAccount.last_login}</div>
                        <div class="categorizer-text hide-mobile">
                            <!-- Bin-->
                            <div style="margin-left: 20px;">
                                <i class="fas fa-trash" onclick="showDeleteAdminAccountModal('${newAdminAccount.identification}')"></i>  
                            </div>  
                        </div>
                    </div>
                `

                bodyToAdd.innerHTML += frame
            });
        }
    })
}
let deletedIntegrationsPageInitialized = false

//entry 
function showStatsIntegrationsPage(){
    var page = document.getElementById("stats-integrations-subpage")
    page.style.display = "grid"

    //initialize page
    if (!deletedIntegrationsPageInitialized){
        initializeIntegrationsStats()
    }
}

//hide deleted integrations page
function hideStatsIntegrationsPage(){
    var page = document.getElementById("stats-integrations-subpage")
    page.style.display = "none"
}

//function to initialize page
function initializeIntegrationsStats(){
    getIntegrationsStats()
}

//function to refresh page
function stats_integrations_page_refresh(object){
    //animate
    if (!object.classList.contains("animate")){
        object.classList.add("animate")
    }
    initializeIntegrationsStats()
}
//get integrations
function getIntegrationsStats(){
    setIntegrationStatsLoader(true)
    //body to display 
    var bodyToDisplay = document.getElementById("IntegrationStatsList")
    bodyToDisplay.innerHTML = ""

    //data 
    data = {
        "project" : localStorage.getItem("working-project") 
    }

    //request
    postToServer("/console/integrations", data, function(responce) {
        setIntegrationStatsLoader(false)
        if (responce == "not found" || responce == "Does'nt seem like the JSON we need"){
            ShowWarning("Error Fetching Objects")
        }
        else{
            //array
            IntegrationObjectList = JSON.parse(responce)
            //iterate through list
            IntegrationObjectList.forEach(jsonObject => {
                var integrationStat = new IntegrationStat(jsonObject)
                var frame = `
                    <!-- item stats-->
                    <div class="stats-integrations-item">
                        <div class="categorizer-text hide-mobile">${integrationStat.identifier}</div>
                        <div class="categorizer-text">${integrationStat.status}</div>
                        <div class="categorizer-text hide-mobile ">${integrationStat.files_stored}</div>
                        <div class="categorizer-text hide-mobile ">${integrationStat.push}</div>
                        <div class="categorizer-text hide-mobile ">${integrationStat.pull}</div>
                        <div class="categorizer-text hide-mobile ">${integrationStat.devices}</div>
                        <div class="categorizer-text hide-mobile ">${integrationStat.daily_average}</div>
                    </div>
                `
                bodyToDisplay.innerHTML += frame
            });

        }
    })

}

//search integrations
function searchIntegrationStat(object){
    if (object.value == ""){
        getIntegrationsStats()
        return
    }
    document.getElementById("IntegrationStatsList").innerHTML = ""
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
    setIntegrationStatsLoader(true)

    data = {
        "project" : localStorage.getItem("working-project"),
        "criteria" : object.value
    }

    postToServer("/console/search-update-integrations",data, function(responce) {
        //hide loading
        setIntegrationStatsLoader(false)
        
        //array
        IntegrationObjectList = JSON.parse(responce)
        //iterate through list
        IntegrationObjectList.forEach(jsonObject => {
            var integrationStat = new IntegrationStat(jsonObject)
            var frame = `
                <!-- item stats-->
                <div class="stats-integrations-item">
                    <div class="categorizer-text hide-mobile">${integrationStat.identifier}</div>
                    <div class="categorizer-text">${integrationStat.status}</div>
                    <div class="categorizer-text hide-mobile ">${integrationStat.files_stored}</div>
                    <div class="categorizer-text hide-mobile ">${integrationStat.push}</div>
                    <div class="categorizer-text hide-mobile ">${integrationStat.pull}</div>
                    <div class="categorizer-text hide-mobile ">${integrationStat.devices}</div>
                    <div class="categorizer-text hide-mobile ">${integrationStat.daily_average}</div>
                </div>
            `

            document.getElementById("IntegrationStatsList").innerHTML += frame
        });
    })
}

//loading 
function setIntegrationStatsLoader(state){
    var loadingModal = document.getElementById("integrationsStatsLoadingModal")
    if(state){
        if (!loadingModal.classList.contains("show")){
            loadingModal.classList.add("show")
        }
        return
    }
    loadingModal.classList.remove("show")
}

//integration class
let IntegrationStat = class {
    constructor(jsonObject){
        this.identifier = jsonObject["identifier"]
        this.push = jsonObject["push"]
        this.pull = jsonObject["pull"]
        this.daily_average = jsonObject["daily_average"]
        //status
        this.status = "Disabled"
        if(jsonObject["enabled"]){
            this.status = "Enabled"
        }
        this.files_stored = jsonObject["files_stored"]
        this.devices = jsonObject["devices"]
    }
}
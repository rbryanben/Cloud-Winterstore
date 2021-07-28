//entry
// after the page has loaded hide the loading modal
// this will show the projects modal
window.document.addEventListener("readystatechange",()=>{
    switch (document.readyState) {
        case "complete":
            setTimeout(function(){
                hideConsoleLoading()
            },1000)
            break;
        }
})

//disable a button 
//this dibles a modal button
function disableModalButton(button){
    button.style.pointerEvents = 'none';
    if (!button.classList.contains("clicked")){
        button.classList.add("clicked")
    }

}

function enableModalButton(button){
    button.style.pointerEvents = 'auto';
    button.classList.remove("clicked")
}

//
//document
function disableScrolling() {
    var x = window.scrollX;
    var y = window.scrollY;
    window.onscroll = function() { window.scrollTo(x, y); };
}

//date converter
function convertDate(dateToConvert){
    if (dateToConvert == null){
        return "No Value"
    }
    try {
        var date = new Date(dateToConvert);
        result  = (date.getDate() + "-" + date.getMonth() + "-" + date.getFullYear() + " " + 
        date.getHours()+":"+date.getMinutes()); 
        return result
    }
    catch(error) {
        return "No Value"
    }
    
}

///keys global
let lockUploadAndDownloadModal = true
let key1 = false
let key2 = false
let optionKey = 0

document.addEventListener('keydown',(event)=>{
    if (event.keyCode == 16){
        key1 = true
    }
    if (event.keyCode == 68){
        key2 = true
        optionKey = 68
    }
    if (event.keyCode == 85){
        key2 = true
        optionKey = 85
    }

    if (key2 && key1 && optionKey == 68 && lockUploadAndDownloadModal == false){
        hideUploads()
        showDownloads()
    }
    if (key2 && key1 && optionKey == 85  && lockUploadAndDownloadModal == false){
        hideDownloads()
        showUploads()
    }
})

document.addEventListener('keyup',(event)=>{
    if (event.keyCode == 16){
        key1 = false
        optionKey = 0
    }
    if (event.keyCode == 68){
        key2 = false
        optionKey = 0
    }
})

//copy element 
function fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;
    
    // Avoid scrolling to bottom
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
  
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
  
    try {
      var successful = document.execCommand('copy');
      var msg = successful ? 'successful' : 'unsuccessful';
      ShowSuccess("Copied File ID")
    } catch (err) {
      console.error('Fallback: Oops, unable to copy', err);
    }
  
    document.body.removeChild(textArea);
}

//handle error
function handleError(error,project){
    console.log(error + " in project " + project)
}

//show demonstration if first time loading project 
window.addEventListener("DOMContentLoaded",()=>{
    if (localStorage.getItem("new-account")){
        //sampling
        initializeDemonstrationModal("demonstationModal")
        var sample_list = []
        sample_list.push(new DemonstrationObject("/static/video/video1.mp4","Open file","Lorem ipsum dolor, sit amet consectetur adipisicing elit. Id sapiente dicta assumenda iure porro minus voluptate vitae consectetur laudantium sit iste facere, deleniti, accusantium reprehenderit error neque possimus perferendis debitis?"))
        sample_list.push(new DemonstrationObject("/static/video/video2.mp4","Close file","Lorem ipsum dolor, sit amet consectetur adipisicing elit. Id sapiente dicta assumenda iure porro minus voluptate vitae consectetur laudantium sit iste facere, deleniti, accusantium reprehenderit error neque possimus perferendis debitis?"))
        sample_list.push(new DemonstrationObject("/static/video/video3.mp4","Rename File" ,"Lorem ipsum dolor, sit amet consectetur adipisicing elit. Id sapiente dicta assumenda iure porro minus voluptate vitae consectetur laudantium sit iste facere, deleniti, accusantium reprehenderit error neque possimus perferendis debitis?"))
        
        //show after loading
        setTimeout(()=>{
            loadDemonstrationModal(sample_list)
        },2000)       
   
    }
})
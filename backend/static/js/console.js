

//Start
window.addEventListener('DOMContentLoaded', function() {
    
    //disable loading
    document.getElementById("loadingModal").style.display = "none"
      
    //should happen after all images have loaded
    setTimeout(() => {
        //loadingModal.style.display = "none"
    }, 1100) 
})


//
//document
function disableScrolling() {
    var x = window.scrollX;
    var y = window.scrollY;
    window.onscroll = function() { window.scrollTo(x, y); };
}

document.addEventListener('keydown',(event)=>{
    if (event.keyCode == 85){
        hideDownloads()
        showUploads()
    }
    else if (event.keyCode == 68){
        hideUploads()
        showDownloads()
    }
})










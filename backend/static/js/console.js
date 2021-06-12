

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

    if (key2 && key1 && optionKey == 68){
        hideUploads()
        showDownloads()
    }
    if (key2 && key1 && optionKey == 85){
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











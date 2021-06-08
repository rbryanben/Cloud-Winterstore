

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








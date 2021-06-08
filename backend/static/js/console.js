

//Start
window.addEventListener('DOMContentLoaded', function() {

    
    //disable loading
    //document.getElementById("loadingModal").style.display = "none"
    
    
    //should happen after all images have loaded
    setTimeout(() => {
            var loadingModal = document.getElementById("loadingModal")
            //complete loading
            var bar = document.getElementById("loadingBar")
            bar.classList.add("finish")
            setTimeout(function(){
                loadingModal.style.display = "none"
            },1100)  
    
    }, 1500) 
})


//
//document
function disableScrolling() {
    var x = window.scrollX;
    var y = window.scrollY;
    window.onscroll = function() { window.scrollTo(x, y); };
}








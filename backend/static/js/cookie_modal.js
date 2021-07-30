window.addEventListener("DOMContentLoaded",()=>{
    var cookieModal = document.getElementById("cookie-modal")
    if (!cookieModal.classList.contains("show") && !localStorage.getItem("showed-cookies")){
        cookieModal.classList.add("show")
    }
})

function markCookieSeen(){
    localStorage.setItem("showed-cookies",true)
    //hide modal
    var cookieModal = document.getElementById("cookie-modal")
    cookieModal.classList.remove("show")
}
window.addEventListener('DOMContentLoaded', function() {

    setTimeout(() => {
        document.querySelector(".loading-modal-body-subtext").innerHTML = "oops! we are still bulding"
    }, 6000)

    document.getElementById("loading-image").onload = function() {
        var modal = document.querySelector(".loading-modal-body")
        modal.classList.add("show")
    }

})
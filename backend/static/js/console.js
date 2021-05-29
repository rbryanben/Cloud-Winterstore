window.addEventListener('DOMContentLoaded', function() {

    setTimeout(() => {
        document.querySelector(".loading-modal-body-subtext").innerHTML = "oops! still building, mean-while  lets consume your CPU"
        window.addEventListener("mousemove", e => {
            var modal = document.querySelector(".loading-modal-body")
            mouseXPercent = e.pageX / window.innerWidth
            mouseYPercentage = e.pageY / window.innerHeight

            //adjustments from the center


            skewX = mouseXPercent * 45
            skewY = mouseYPercentage * 45

            modal.style.transform = "rotateY(" + skewX + "deg)"
            modal.style.transform = "rotateX(" + skewY + "deg)"
            modal.style.transform = "rotateZ(" + -skewY + "deg)"

        })
    }, 6000)

    document.getElementById("loading-image").onload = function() {
        var modal = document.querySelector(".loading-modal-body")
        modal.classList.add("show")
    }



    function getRandomInt(max) {
        return Math.floor(Math.random() * 5);
    }
})
function dimPager() {
    var pagerBody = document.getElementById("pagerBody")
    if (!pagerBody.classList.contains("dim")) {
        pagerBody.classList.add("dim")
    }
}

function unDimPager() {
    var pagerBody = document.getElementById("pagerBody")
    if (pagerBody.classList.contains("dim")) {
        pagerBody.classList.remove("dim")
    }
}


function showLoginModal() {
    var loginModal = document.getElementById("loginModal")
        //show modal 
    if (!loginModal.classList.contains("show")) {
        loginModal.classList.add("show")
        disableScrolling()
    }
    dimPager();
}

function hideLoginModal() {
    var loginModal = document.getElementById("loginModal")
    if (loginModal.classList.contains("show")) {
        loginModal.classList.remove("show")
        enableScrolling()
        unDimPager();
    }
}

function disableScrolling() {
    var x = window.scrollX;
    var y = window.scrollY;
    window.onscroll = function() { window.scrollTo(x, y); };
}

function enableScrolling() {
    window.onscroll = function() {};
}

//function to call login 
function login() {
    username = document.getElementById("loginUsername").value
    password = document.getElementById("loginPassword").value
        //put credentials into json
    var credentials = {
            "username": username,
            "password": password
        }
        //attempt login
    postToServer("/login", credentials, function(responce) {
        if (responce == "200") {
            ShowSuccess("Login Successful")
        } else {
            ShowWarning("Login Failed")
        }
    })

}


//notification functions 
window.addEventListener('DOMContentLoaded', (event) => {});


function ShowWarning(text) {
    var waringNotification = `
    <div class="notification">
        <div class="notification-icon">
            <i class="fas fa-exclamation-triangle" style="color: yellow; margin-right: 10px;"></i>` + text + `
        </div>
    </div>
    `;

    document.getElementById("notificationContainer").innerHTML = waringNotification;
}

function ShowSuccess(text) {
    var waringNotification = `
    <div class="notification">
        <div class="notification-icon">
        <i class="fas fa-check" style="color: rgb(77, 179, 63); margin-right: 10px;"></i>` + text + `
        </div>
    </div>
    `;

    document.getElementById("notificationContainer").innerHTML = waringNotification;
}

////
//// This function goes to a page
function goto(url) {
    window.location.href = (url)
}

///
///function to show loader 
function showLoading() {
    var loader = document.getElementById("loader")
    if (!loader.classList.contains("show")) {
        loader.classList.add("show")
    }
    disableScrolling()
}

function hideLoading() {
    document.getElementById("loader").style.visibility = "hidden"
    loader.classList.remove("show")
    enableScrolling()
}
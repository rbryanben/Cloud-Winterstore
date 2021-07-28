//start
'{% load static %}'
window.addEventListener('DOMContentLoaded', () => {
    preloadObjects([serverURL + "/static/png/logo.png"]); //preload loading image and background
})


//
//modals
function showLoginModal() {
    //check authentication
    if (!isAuthenticated) {
        postToServer("/checkAuthentication", null, function(responce) {
            if (responce == "200") {
                goto("/console/")
            }
        })
    }

    if (isAuthenticated) {
        goto("/console/")
        return
    }


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

//
//document
function disableScrolling() {
    var x = window.scrollX;
    var y = window.scrollY;
    window.onscroll = function() { window.scrollTo(x, y); };
}

function enableScrolling() {
    window.onscroll = function() {};
}

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


//authentication
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
            setTimeout(() => {
                goto("/console/")
            }, 2000)
            ShowSuccess("Login Successful")
        } else {
            ShowWarning("Login Failed")
        }
    })

}

let isAuthenticated = false;

postToServer("/checkAuthentication", null, function(responce) {
    if (responce == "200") {
        isAuthenticated = true
    } else {
        isAuthenticated = false
    }
})


//
// alerts

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
//// relocation
function goto(url) {
    window.location.href = (url)
}

///
/// loader
function showLoading() {
    //make notification block visible 
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



//
//communication
function postToServer(url, data, callback) {
    var serverURL = window.location.origin;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(xmlhttp.response);
        }
    }

    xmlhttp.open("POST", serverURL + url)
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.send(JSON.stringify(data));

}

//
//cache
function preloadObjects(array) {
    if (!preloadImages.list) {
        preloadImages.list = [];
    }
    var list = preloadImages.list;
    for (var i = 0; i < array.length; i++) {
        var img = new Image();
        img.onload = function() {
            var index = list.indexOf(this);
            if (index !== -1) {
                // remove image from the array once it's loaded
                // for memory consumption reasons
                list.splice(index, 1);
            }
        }
        list.push(img);
        img.src = array[i];
    }
}
//first function to trigger
window.addEventListener("DOMContentLoaded", function() {
    watchUsername();
    watchPassword();
    watchEmail();
    watchTerms();
})



//watches inputs 
function watchEmail() {
    var emailInput = document.getElementById("signupEmailInput")
    emailInput.addEventListener("keyup", (event) => {
        if (!validateEmail(emailInput.value)) {
            if (!emailInput.classList.contains("error")) {
                emailInput.classList.add("error")

            }
            emailPass = false;
        } else {
            emailInput.classList.remove("error")
            emailPass = true;
        }
        hjdenunyGJn({
            "email": emailInput.value
        })
    })

}

function watchUsername() {
    var usernameInput = document.getElementById("signupUsernameInput")
    usernameInput.addEventListener("keyup", (event) => {
        if (usernameInput.value.length > 7) {
            xhjKilYuiak({
                "username": usernameInput.value
            })
        }
    })
}

function watchPassword() {
    var passwordBox = document.getElementById("signupPasswordInput");
    passwordBox.addEventListener("keyup", (event) => {
        StrengthChecker(passwordBox.value)
    })
}

function watchTerms() {
    var termsInput = document.getElementById("signupTermsInput")
    termsInput.addEventListener("click", function() {
        if (termsInput.checked) {
            termsPass = true;
        } else {
            termsPass = false;
        }
    })
}


//checks on server requests
function xhjKilYuiak(data) {
    var usernameInput = document.getElementById("signupUsernameInput")
    postToServer("/hjkdjNHjnudellphgy", data, function(responce) {
        if (responce == "500") {
            if (!usernameInput.classList.contains("error")) {
                usernameInput.classList.add("error")

            }
            usernamePass = false;
        } else {
            usernameInput.classList.remove("error")
            usernamePass = true;
        }
    })
}

function hjdenunyGJn(data) {
    var emailInput = document.getElementById("signupEmailInput")
    postToServer("/hudiueiewfefrefrde", data, function(responce) {
        if (responce == "500") {
            if (!emailInput.classList.contains("error")) {
                emailInput.classList.add("error")
                emailPass = false;
            }
        } else {
            if (emailPass) {
                emailInput.classList.remove("error")
                emailPass = true;
            }
        }
    })
}

///checking that everything checksup 
let usernamePass = false
let emailPass = false
let passwordPass = false
let termsPass = false

//validations 
let strongPassword = new RegExp('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})')
let mediumPassword = new RegExp('((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,}))|((?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])(?=.{8,}))')

function StrengthChecker(PasswordParameter) {
    var passwordBox12 = document.getElementById("signupPasswordInput")

    // We then change the badge's color and text based on the password strength
    var passwordStrengthMeter = document.getElementById("passwordStrengthMeter")
    passwordStrengthMeter.style.color = "white"
    if (strongPassword.test(PasswordParameter)) {
        passwordStrengthMeter.innerHTML = "Strong"
        removeAllClassListsFromStrengthCheckerAndAdd("strong")
        passwordBox12.classList.remove("error")
        passwordPass = true;

    } else if (mediumPassword.test(PasswordParameter)) {
        passwordStrengthMeter.innerHTML = "Medium"
        removeAllClassListsFromStrengthCheckerAndAdd("medium")
        passwordBox12.classList.remove("error")
        passwordPass = true;
    } else {
        passwordStrengthMeter.innerHTML = "Weak"
        removeAllClassListsFromStrengthCheckerAndAdd("weak")
        if (!passwordBox12.classList.contains("error")) {
            passwordBox12.classList.add("error")
            passwordPass = false;
        }
    }


    function removeAllClassListsFromStrengthCheckerAndAdd(item) {
        passwordStrengthMeter.classList.remove("strong")
        passwordStrengthMeter.classList.remove("weak")
        passwordStrengthMeter.classList.remove("medium")
            ///show error on input component if password is weak

        passwordStrengthMeter.classList.add(item)
    }
}

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}



//signup 
function signupFreeClient() {
    var usernameInput = document.getElementById("signupUsernameInput")
    var emailInput = document.getElementById("signupEmailInput")
    var passwordBox = document.getElementById("signupPasswordInput");

    if (usernamePass && passwordPass && termsPass && emailPass) {
        showLoading();

        //data to be posted
        //dont worry I am checking on the server side too
        data = {
            "username": usernameInput.value,
            "email": emailInput.value,
            "password": passwordBox.value
        }
        postToServer("/new-free-user", data, function(responce) {
            if (responce != "500") {
                hideLoading()
                ShowSuccess("Verification Link Sent")
                setTimeout(function() {
                    window.location.replace("/verify/" + responce)
                }, 2000)

            } else {
                hideLoading()
                ShowWarning("Failed to Send Verification Link")
            }
        })

    } else {
        //alert user where problem is 
        if (!usernamePass) {
            ShowWarning("Check Username")
            return
        }
        if (!passwordPass) {
            ShowWarning('Check Password')
            return
        }
        if (!termsPass) {
            ShowWarning('Please Agree to Terms')
            return
        }
        if (!emailPass) {
            ShowWarning('Check Email')
            return;
        }
    }
}


//signup 
function signupEnhancedClient() {
    var usernameInput = document.getElementById("signupUsernameInput")
    var emailInput = document.getElementById("signupEmailInput")
    var passwordBox = document.getElementById("signupPasswordInput");

    if (usernamePass && passwordPass && termsPass && emailPass) {
        showLoading();

        //data to be posted
        //dont worry I am checking on the server side too
        data = {
            "username": usernameInput.value,
            "email": emailInput.value,
            "password": passwordBox.value,
        }
        postToServer("/new-free-user", data, function(responce) {
            if (responce != "500") {
                hideLoading()
                ShowSuccess("Verification Link Sent")
                setTimeout(function() {
                    localStorage.setItem("enhanced", true) //store that this is enhanced
                    window.location.replace("/verify/" + responce)
                }, 2000)

            } else {
                hideLoading()
                ShowWarning("Failed to Send Verification Link")
            }
        })

    } else {
        //alert user where problem is 
        if (!usernamePass) {
            ShowWarning("Check Username")
            return
        }
        if (!passwordPass) {
            ShowWarning('Check Password')
            return
        }
        if (!termsPass) {
            ShowWarning('Please Agree to Terms')
            return
        }
        if (!emailPass) {
            ShowWarning('Check Email')
            return;
        }
    }
}
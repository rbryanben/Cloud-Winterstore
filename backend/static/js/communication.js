//this is the global server url
let serverURL = window.location.origin;


function postToServer(url, data, callback) {
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
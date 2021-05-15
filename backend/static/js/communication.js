function postToServer(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.warn(xmlhttp.response)
            callback(xmlhttp.response);
        }
    }

    xmlhttp.open("POST", url)
    xmlhttp.setRequestHeader('Content-Type', 'application/json');

    xmlhttp.send(JSON.stringify(data));
}
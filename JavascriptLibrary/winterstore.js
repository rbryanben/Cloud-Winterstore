let CloudWinterstoreConnection = class {
    constructor(username,password){
        this.username = username
        this.password = password
        this.authenticate()
    }

    static WinterstoreURL = "http://192.168.1.6"
    
    //test connection
    testConnection(){
        PostToCloudWinterstore("/api/gateway/",{},(responce)=>{
            console.warn(responce)
        })
    }

    //authenticate 
    authenticate(){
        PostToCloudWinterstore("/login",{"username":this.username,"password":this.password},(response)=>{
            if (response == "200"){
                console.warn("authenticated")
            }
            else {
                console.warn("authentication failed")
            }
        })
    }


    //download file
    downloadFile(key){
        PostToCloudWinterstoreBlob("/console/get-file",{"id" : key},(response)=>{
            
            a = document.createElement('a');
                a.href = window.URL.createObjectURL(response);
                console.warn(a.href)
                // Give filename you wish to download
                a.download = "file";
                a.style.display = 'none';
                document.body.appendChild(a);
                a.click();
        })
    }
}


function PostToCloudWinterstoreBlob(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(xmlhttp.response);
        }
    }



    xmlhttp.open("POST", CloudWinterstoreConnection.WinterstoreURL + url)
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.send(JSON.stringify(data));
    xmlhttp.responseType = 'blob';
}


function PostToCloudWinterstore(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            callback(xmlhttp.response);
        }
    }

    xmlhttp.open("POST", CloudWinterstoreConnection.WinterstoreURL + url)
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.send(JSON.stringify(data));
}







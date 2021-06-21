let CloudWinterstoreConnection = class {
    constructor(username,password){
        this.username = username
        this.password = password
        this.authenticate()
    }

    static WinterstoreURL = "http://cloudwinterstore.ddns.net"
    
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
    downloadFile(filekey,filename){
        key = filekey
        PostToCloudWinterstoreBlob("/api/download/"+key,{"id" : key},(response)=>{
            var blob = new Blob([response],null)
            var downloadURL = URL.createObjectURL(blob)
            var fileToDownload = document.createElement("a");
            fileToDownload.href = downloadURL
            fileToDownload.download = filename
            document.body.appendChild(fileToDownload)
            fileToDownload.click()
        })
    }


    //insert file into element 
    setMediaOfElement(element,filekey){
        element.src = CloudWinterstoreConnection.WinterstoreURL+'/api/download/'+filekey
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







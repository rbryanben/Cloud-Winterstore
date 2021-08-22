package com.wapazockdemo.winterstoreconnector.utils;

import androidx.annotation.NonNull;

import com.bumptech.glide.RequestBuilder;
import com.wapazockdemo.winterstoreconnector.interfaces.ConnectionInterface;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;

public class Connection {

    //server urls
    private String serverURL = "http://192.168.1.5:80";
    private String getTokenURL =  serverURL + "/api/get-token";

    //variables
    private ConnectionInterface connectionInterface;
    private Credentials clientCredentials;
    public static final MediaType JSON = MediaType.get("application/json; charset=utf-8");

    //constructor with credentials
    public Connection(@NonNull ConnectionInterface connectionInterface,@NonNull Credentials credentials){
        this.connectionInterface = connectionInterface;
        this.clientCredentials = credentials;
    }

    //get token
    private void getToken() throws Exception {
        //client
        OkHttpClient client = new OkHttpClient();

        //request body
        RequestBody clientBody = RequestBody.create(JSON,clientCredentials.asJSON().toString());

        //request
        Request request = new Request.Builder()
                .url()
    }
}

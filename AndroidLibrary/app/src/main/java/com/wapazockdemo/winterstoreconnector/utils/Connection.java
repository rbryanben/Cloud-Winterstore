package com.wapazockdemo.winterstoreconnector.utils;

import android.app.Activity;
import android.app.Application;
import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.NonNull;

import com.bumptech.glide.RequestBuilder;
import com.wapazockdemo.winterstoreconnector.MainActivity;
import com.wapazockdemo.winterstoreconnector.interfaces.ConnectionInterface;

import org.jetbrains.annotations.NotNull;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class Connection {
    // TAG
    public static String TAG = "Connection";

    //server urls
    private String serverURL = "http://192.168.1.5:80";
    private String getTokenURL =  serverURL + "/api/get-token/";
    private Activity activity;

    //variables
    private ConnectionInterface connectionInterface;
    private Credentials clientCredentials;
    private Context context;
    public static final MediaType JSON = MediaType.get("application/json; charset=utf-8");


    //constructor with credentials
    public Connection(@NonNull ConnectionInterface connectionInterface,@NonNull Credentials credentials, Activity activity){
        this.connectionInterface = connectionInterface;
        this.clientCredentials = credentials;
        this.activity = activity;

        //get token
        try {
            getToken();
        }
        catch (Exception e){
            e.printStackTrace();

            //show that a fatal error
            connectionInterface.connectionFailed("Fatal Error");
        }
    }

    //get token
    private void getToken() throws Exception {
        //client
        OkHttpClient client = new OkHttpClient();

        //request body
        RequestBody clientBody = RequestBody.create(JSON,clientCredentials.asJSON().toString());

        //request
        Request request = new Request.Builder()
                .url(getTokenURL)
                .post(clientBody)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                connectionInterface.connectionFailed("Network Error");
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                //result from the server
                String result = response.body().string();

                //callback
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        connectionInterface.tokenReceived(result);
                    }
                });

            }
        });
    }
}

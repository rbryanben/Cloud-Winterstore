package com.wapazockdemo.winterstoreconnector.utils;

import android.app.Activity;
import android.content.Context;
import android.util.Log;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.load.model.GlideUrl;
import com.bumptech.glide.load.model.LazyHeaders;
import com.wapazockdemo.winterstoreconnector.interfaces.ConnectionInterface;
import org.jetbrains.annotations.NotNull;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static com.bumptech.glide.load.resource.drawable.DrawableTransitionOptions.withCrossFade;

public class Connection {
    // TAG
    public static String TAG = "Connection";

    //server urls
    private String serverURL = "http://192.168.1.5:80";
    private String getTokenURL =  serverURL + "/api/get-token/";
    private String downloadURL = serverURL + "/api/download/";


    //variables
    private Activity activity;
    private ConnectionInterface connectionInterface;
    private Credentials clientCredentials;
    private Context context;
    private String TOKEN;
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

    // This method gets the clients token from the server
    // Upon getting a response, it either calls the receivedToken interface or connectionError interface
    // It also assigns the Token as the token variable in this class.
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
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        connectionInterface.connectionFailed("Network Error");
                    }
                });

            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                //if response is not successful, server unreachable
                if (!response.isSuccessful()) {
                    activity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            connectionInterface.connectionFailed("Server Unreachable");
                        }
                    });
                }

                //result from the server
                String result = response.body().string();

                //callback
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        //check response
                        switch (result){
                            case "Invalid JSON":
                                connectionInterface.connectionFailed(result);
                                break;
                            case "denied":
                                connectionInterface.connectionFailed("Invalid Credentials");
                                break;
                            case "not found":
                                connectionInterface.connectionFailed("Not Found");
                                break;
                            default:
                                TOKEN = result;
                                connectionInterface.tokenReceived(result);
                                break;
                        }
                    }
                });

            }
        });
    }


    // get file by id
    // returns the bytes of that file
    public void getFile(String id, File file){
        // client
        OkHttpClient client = new OkHttpClient();

        // request
        Request request = new Request.Builder()
                .url(compileDownloadURL(id))
                .addHeader("Authorization","Token " + TOKEN)
                .build();

        // request
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        connectionInterface.connectionFailed("Network Error");
                    }
                });
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                //if response is not successful, server unreachable
                if (!response.isSuccessful()) {
                    activity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            connectionInterface.connectionFailed("Server Unreachable");
                        }
                    });
                }

                //keep bytes
                byte[] result = response.body().bytes();

                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // stream
                        try {
                            FileOutputStream stream = new FileOutputStream(file);
                            stream.write(result);
                            stream.close();
                            connectionInterface.fileSaved(file);
                        } catch (FileNotFoundException e) {
                            connectionInterface.fileError("File Not Found");
                        } catch (IOException e) {
                            connectionInterface.fileError("Failed To Write File");
                        }
                    }
                });
            }
        });
    }


    // Load Image: Given an object to display the image, assigns the given
    // imageID as the image received from the server
    public void loadImage(ImageView imageView, String imageID){
        // Custom Headers for Glide Request
        GlideUrl url = new GlideUrl(compileDownloadURL(imageID), new LazyHeaders.Builder()
                .addHeader("Authorization", "Token " + TOKEN)
                .build());

        // Load the image
        Glide.with(activity)
                .load(url)
                .diskCacheStrategy(DiskCacheStrategy.NONE)
                .into(imageView);
    }



    // Get URL - Given a file id, returns the final URL for the file
    private String compileDownloadURL(String id){
        return  downloadURL + id ;
    }
}

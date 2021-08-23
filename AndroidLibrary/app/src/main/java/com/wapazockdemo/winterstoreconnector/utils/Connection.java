package com.wapazockdemo.winterstoreconnector.utils;

import android.app.Activity;
import android.content.Context;
import android.widget.ImageView;
import androidx.annotation.NonNull;
import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.load.model.GlideUrl;
import com.bumptech.glide.load.model.LazyHeaders;
import com.wapazockdemo.winterstoreconnector.interfaces.ConnectionInterface;
import org.jetbrains.annotations.NotNull;
import org.json.JSONObject;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class Connection {
    // TAG
    public static String TAG = "Connection";

    //server urls
    private String serverURL = "https://cloudwinterstore.co.zw";
    private String getTokenURL =  serverURL + "/api/get-token/";
    private String downloadURL = serverURL + "/api/download/";
    private String createFolderURL = serverURL + "/api/create-client-folder";
    private String uploadURL = serverURL + "/api/upload-file/";
    private String deleteURL = serverURL + "/api/client-delete-index-object/";
    private String giveKeyURL = serverURL + "/api/client-give-key/";
    private String removeKeysURL = serverURL + "/api/client-remove-keys/";
    private String getFolderURL = serverURL + "/api/client-get-folder/";
    private String fileInfoURL = serverURL + "/api/client-file-info/";

    //variables
    private Activity activity;
    private ConnectionInterface connectionInterface;
    private Credentials clientCredentials;
    private Context context;
    private String TOKEN;
    public static final MediaType JSON = MediaType.get("application/json; charset=utf-8");


    //constructor with credentials
    public Connection( Activity activity, @NonNull Credentials credentials,@NonNull ConnectionInterface connectionInterface){
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

    // Create Folder: Creates a folder in the client's project given
    // the parentID and the FolderName
    public void createFolder(String parentID,String folderName){
        // Client
        OkHttpClient client = new OkHttpClient();

        // Data to send
        JSONObject newDataObject = new JSONObject();
        try {
            newDataObject.put("parentID", parentID);
            newDataObject.put("folderName", folderName);
        }
        catch (Exception e){
            e.printStackTrace();
        }

        // Body
        RequestBody body = RequestBody.create(JSON,newDataObject.toString());

        // Request
        Request request = new Request.Builder()
                .url(createFolderURL)
                .post(body)
                .addHeader("Authorization","Token " + TOKEN)
                .build();

        // Send request
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

                //result
                String result = response.body().string();

                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        switch (result) {
                            case "Invalid JSON":
                                connectionInterface.connectionFailed(result);
                                break;
                            case  "1701":
                                connectionInterface.connectionFailed("Folder Already Exists");
                            case "denied":
                                connectionInterface.connectionFailed(result);
                                break;
                            default:
                                connectionInterface.folderCreated(result);
                        }
                    }
                });
            }
        });
    }

    // Upload File: Uploads to a folder in the client's project, given
    // a file, name, parentFolder, accessControl and integration
    public void uploadFile(File file, String name,Boolean allowAllUsersWrite, Boolean allowAllUsersRead, Boolean allowKeyUsersRead,
                           Boolean allowKeyUsersWrite, String integration,String parent, int uploadID)
    {
        //calculate size
        long size = file.getAbsoluteFile().length();

        // client
        OkHttpClient client = new OkHttpClient();

        // multipart form body
        RequestBody requestBody = new MultipartBody.Builder().setType(MultipartBody.FORM)
                .addFormDataPart("file", file.getName(),
                        RequestBody.create(MediaType.parse("text/csv"), file))
                .addFormDataPart("name", name)
                .addFormDataPart("allowAllUsersWrite", String.valueOf(allowAllUsersWrite))
                .addFormDataPart("allowAllUsersRead", String.valueOf(allowAllUsersRead))
                .addFormDataPart("allowKeyUsersWrite", String.valueOf(allowKeyUsersWrite))
                .addFormDataPart("allowKeyUsersRead", String.valueOf(allowKeyUsersRead))
                .addFormDataPart("integration",integration)
                .addFormDataPart("parent",parent)
                .addFormDataPart("size", String.valueOf(size))
                .build();
        
        // request
        Request request = new Request.Builder()
                .post(requestBody)
                .url(uploadURL)
                .addHeader("Authorization","Token " + TOKEN)
                .build();
        
        // send request
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
                // If the upload was not successful
                if (!response.isSuccessful()){
                    activity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            connectionInterface.connectionFailed("Server Unreachable");
                        }
                    });
                }

                //keep the result in a variable
                String result = response.body().string();
                int uploadIdentification = uploadID;


                //if the request was successful
                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        switch (result) {
                            case "woahh - does'nt seem like the data we need -- Invalid form data":
                                connectionInterface.uploadResults(uploadIdentification,false,"Invalid Form");
                                break;
                            case  "1703":
                                connectionInterface.uploadResults(uploadIdentification,false,"Filename Exist");
                                break;
                            case "500":
                                connectionInterface.uploadResults(uploadIdentification,false,"Error");
                                break;
                            case "1702":
                                connectionInterface.uploadResults(uploadIdentification,false,"Bad Filename");
                                break;
                            case "not found":
                                connectionInterface.uploadResults(uploadIdentification,false,"Invalid Integration");
                                break;
                            default:
                                connectionInterface.uploadResults(uploadIdentification,true,result);
                                break;
                        }
                    }
                });

            }
        });
    }

    // Delete Index Object: Deletes an index object given the id
    //  of the object
    public void deleteIndexObject(String id){
        //Client
        OkHttpClient client = new OkHttpClient();

        //data to send
        JSONObject data = new JSONObject();
        try{
            data.put("id",id);
        }
        catch (Exception e){
            e.printStackTrace();
        }

        // Request Body
        RequestBody body = RequestBody.create(JSON,data.toString());

        // Request
        Request request = new Request.Builder()
                .url(deleteURL)
                .addHeader("Authorization","Token " + TOKEN)
                .post(body)
                .build();

        // Send the request
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
                // If the upload was not successful
                if (!response.isSuccessful()){
                    activity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            //server unreachable
                            connectionInterface.deleteResults(id,false,"Server Unreachable");
                        }
                    });
                }

                //keep the result in a variable
                String result = response.body().string();

                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        switch (result){
                            case  "Hey! This does'nt look like the json file we need -- The JSON supplied is invalid":
                                connectionInterface.deleteResults(id,false,"Invalid JSON");
                                break;
                            case "Not Found":
                                connectionInterface.deleteResults(id,false,"not found");
                                break;
                            case "denied":
                                connectionInterface.deleteResults(id,false,"denied");
                                break;
                            default:
                                connectionInterface.deleteResults(id,true,id);
                        }
                    }
                });

            }
        });
    }


    // Give Key: This method gives a key to another client
    public void giveKey(String clientAccount, String fileID){
        //Client
        OkHttpClient client = new OkHttpClient();

        //data to send
        JSONObject data = new JSONObject();
        try{
            data.put("account",clientAccount);
            data.put("file",fileID);
        }
        catch (Exception e){
            e.printStackTrace();
        }

        // Request Body
        RequestBody body = RequestBody.create(JSON,data.toString());

        // Request
        Request request = new Request.Builder()
                .url(giveKeyURL)
                .addHeader("Authorization","Token " + TOKEN)
                .post(body)
                .build();

        // Send the request
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
                // If the upload was not successful
                if (!response.isSuccessful()){
                    activity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            //server unreachable
                            connectionInterface.giveKeyResults(clientAccount,false,"Server Unreachable");
                        }
                    });
                }

                //keep the result in a variable
                String result = response.body().string();

                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        switch (result){
                            case  "500":
                                connectionInterface.giveKeyResults(clientAccount,false,"Invalid JSON");
                                break;
                            case "not found":
                                connectionInterface.giveKeyResults(clientAccount,false,"not found");
                                break;
                            case "denied":
                                connectionInterface.giveKeyResults(clientAccount,false,"denied");
                                break;
                            default:
                                connectionInterface.giveKeyResults(clientAccount,true,clientAccount);
                        }
                    }
                });

            }
        });
    }

    // Give Key: This method gives a key to another client
    public void removeKeys(String clientAccount, String fileID){
        //Client
        OkHttpClient client = new OkHttpClient();

        //data to send
        JSONObject data = new JSONObject();
        try{
            data.put("account",clientAccount);
            data.put("file",fileID);
        }
        catch (Exception e){
            e.printStackTrace();
        }

        // Request Body
        RequestBody body = RequestBody.create(JSON,data.toString());

        // Request
        Request request = new Request.Builder()
                .url(removeKeysURL)
                .addHeader("Authorization","Token " + TOKEN)
                .post(body)
                .build();

        // Send the request
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
                // If the upload was not successful
                if (!response.isSuccessful()){
                    activity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            //server unreachable
                            connectionInterface.removeKeysResults(clientAccount,false,"Server Unreachable");
                        }
                    });
                }

                //keep the result in a variable
                String result = response.body().string();

                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        switch (result){
                            case  "500":
                                connectionInterface.removeKeysResults(clientAccount,false,"Invalid JSON");
                                break;
                            case "not found":
                                connectionInterface.removeKeysResults(clientAccount,false,"not found");
                                break;
                            case "denied":
                                connectionInterface.removeKeysResults(clientAccount,false,"denied");
                                break;
                            default:
                                connectionInterface.removeKeysResults(clientAccount,true,"200");
                        }
                    }
                });

            }
        });
    }

    // File Info: Gets information on a file given a file id
    public void fileInfo(String fileID){
        //Client
        OkHttpClient client = new OkHttpClient();

        //data to send
        JSONObject data = new JSONObject();
        try{
            data.put("id",fileID);
        }
        catch (Exception e){
            e.printStackTrace();
        }

        // Request Body
        RequestBody body = RequestBody.create(JSON,data.toString());

        // Request
        Request request = new Request.Builder()
                .url(fileInfoURL)
                .addHeader("Authorization","Token " + TOKEN)
                .post(body)
                .build();

        // Send the request
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
                // If the upload was not successful
                if (!response.isSuccessful()){
                    activity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            //server unreachable
                            connectionInterface.fileInfoResults(fileID,false,"Server Unreachable");
                        }
                    });
                }

                //keep the result in a variable
                String result = response.body().string();

                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        switch (result){
                            case  "Does'nt seem like the json we need":
                                connectionInterface.fileInfoResults(fileID,false,"Invalid JSON");
                                break;
                            case "not found":
                                connectionInterface.fileInfoResults(fileID,false,"not found");
                                break;
                            case "denied":
                                connectionInterface.fileInfoResults(fileID,false,"denied");
                                break;
                            case "Not File":
                                connectionInterface.fileInfoResults(fileID,false,"Not File");
                                break;
                            default:
                                connectionInterface.fileInfoResults(fileID,true,result);
                        }
                    }
                });

            }
        });
    }

    // File Info: Gets information on a file given a file id
    public void listFolder(String folderID){
        //Client
        OkHttpClient client = new OkHttpClient();

        //data to send
        JSONObject data = new JSONObject();
        try{
            data.put("folderID",folderID);
        }
        catch (Exception e){
            e.printStackTrace();
        }

        // Request Body
        RequestBody body = RequestBody.create(JSON,data.toString());

        // Request
        Request request = new Request.Builder()
                .url(getFolderURL)
                .addHeader("Authorization","Token " + TOKEN)
                .post(body)
                .build();

        // Send the request
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
                // If the upload was not successful
                if (!response.isSuccessful()){
                    activity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            //server unreachable
                            connectionInterface.getFolderResults(folderID,false,"Server Unreachable");
                        }
                    });
                }

                //keep the result in a variable
                String result = response.body().string();

                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        switch (result){
                            case  "doesn't seem like json data":
                                connectionInterface.getFolderResults(folderID,false,"Invalid JSON");
                                break;
                            case "Folder Not Found":
                                connectionInterface.getFolderResults(folderID,false,"not found");
                                break;
                            case "denied":
                                connectionInterface.getFolderResults(folderID,false,"denied");
                                break;
                            default:
                                connectionInterface.getFolderResults(folderID,true,result);
                        }
                    }
                });

            }
        });
    }

    // Get URL - Given a file id, returns the final URL for the file
    private String compileDownloadURL(String id){
        return  downloadURL + id ;
    }
}

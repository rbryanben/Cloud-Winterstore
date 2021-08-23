package com.wapazockdemo.winterstoreconnector;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.media.Image;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.wapazockdemo.winterstoreconnector.interfaces.ConnectionInterface;
import com.wapazockdemo.winterstoreconnector.utils.Connection;
import com.wapazockdemo.winterstoreconnector.utils.Credentials;

import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.time.ZoneId;

public class MainActivity extends AppCompatActivity {
    // TAG
    public static String TAG = "MainActivity";

    //Variables
    ImageView myImage;
    Connection connection;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //set variables
        myImage = findViewById(R.id.myImageView);

        //Credentials
        Credentials credentials = new Credentials("client@cloudwinterstore.co.zw","password25","19FJ221PWTOOO546X35LMIT5RPJQ4E4QFR4TZN");

        //bind connection
        bindConnection(credentials);
    }

    // This method bind the connection to Cloud
    private void bindConnection(Credentials credentials){
        connection = new Connection(MainActivity.this, credentials, new ConnectionInterface() {
            @Override
            public void tokenReceived(String token) {
                //download a video
                connection.getFile("EWFXY954SEO5FF4JTNVFAVQSG7AKO6PE1ZST9YJRKJ9HQ160QT829FEPWW30KOGX",new File(getExternalFilesDir("Images"),"cat.jpg"));
            }

            @Override
            public void connectionFailed(String error) {

            }

            @Override
            public void fileSaved(File file) {
                connection.uploadFile(file,"cat.jpg",true,true,true,true,"19FJ221PWTOOO546X35LMIT5RPJQ4E4QFR4TZN","66TCW7Q9BGLIFEJLBN4PYNLOGO3P2TP82MKQO1RQX2FMSRIDJWLNHK32K9YKZHE6",23);
            }

            @Override
            public void fileError(String error) {

            }

            @Override
            public void folderCreated(String id) {

            }

            @Override
            public void uploadResults(int uploadID, Boolean wasSuccessful, String result) {
                Toast.makeText(MainActivity.this,"Upload Result: "+result,Toast.LENGTH_LONG).show();
            }


        });
    }


}
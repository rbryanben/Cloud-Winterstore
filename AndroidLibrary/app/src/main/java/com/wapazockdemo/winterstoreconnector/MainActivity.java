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

public class MainActivity extends AppCompatActivity implements ConnectionInterface {
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

        //test credentials
        Credentials credentials = new Credentials("client@cloudwinterstore.co.zw","password25","19FJ221PWTOOO546X35LMIT5RPJQ4E4QFR4TZN");

        // create a connection
        connection = new Connection(this,credentials,this);

    }

    @Override
    public void tokenReceived(String token) {
        // get bytes
        connection.getFile("6S7JTYSRIMBWTI8QUH0HGADT8TC48M1DGMOX3U0QM0IIK5C0OPP8A4YML4H2NPCC",new File(getExternalFilesDir("Images"),"coolCat.jpg"));
    }

    @Override
    public void connectionFailed(String error) {
        Toast.makeText(this,"Connection Error: "+error,Toast.LENGTH_LONG).show();
    }

    @Override
    public void fileSaved(File file) {
        Toast.makeText(this,"File Saved: "+file.getName(),Toast.LENGTH_LONG).show();
        Glide.with(this)
                .load(file)
                .diskCacheStrategy(DiskCacheStrategy.NONE)
                .into(myImage);

    }

    @Override
    public void fileError(String error) {
        Toast.makeText(this,"File Error: "+error,Toast.LENGTH_LONG).show();
    }


}
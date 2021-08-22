package com.wapazockdemo.winterstoreconnector;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //test credentials
        Credentials credentials = new Credentials("client@cloudwinterstore.co.zw","password25","19FJ221PWTOOO546X35LMIT5RPJQ4E4QFR4TZN");

        // create a connection
        Connection connection = new Connection(this,credentials,this);

    }

    @Override
    public void tokenReceived(String token) {
        Toast.makeText(this,"Token: "+token,Toast.LENGTH_LONG).show();
    }

    @Override
    public void connectionFailed(String error) {

    }
}
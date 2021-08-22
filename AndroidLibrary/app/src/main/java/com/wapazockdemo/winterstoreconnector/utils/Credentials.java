package com.wapazockdemo.winterstoreconnector.utils;

import org.json.JSONObject;

import java.security.spec.ECField;

public class Credentials {

    //variables
    private String username,password,integration;

    //get username, which can be used to check who the client is
    public String getUsername() {
        return username;
    }

    //constructor
    public Credentials(String username, String password, String integration) {
        this.username = username;
        this.password = password;
        this.integration = integration;
    }

    //return a JSON object
    public JSONObject asJSON() throws Exception {
        //create a new JSON object
        JSONObject newJSONObject = new JSONObject();
        newJSONObject.put("username",this.username);
        newJSONObject.put("password",this.password);
        newJSONObject.put("integration",this.integration);

        //return the JSON object
        return  newJSONObject;
    }
}

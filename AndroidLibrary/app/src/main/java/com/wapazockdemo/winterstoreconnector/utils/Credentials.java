package com.wapazockdemo.winterstoreconnector.utils;

import org.json.JSONObject;

import java.security.spec.ECField;

public class Credentials {

    //variables
    private String username,password;

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    //return a JSON object
    public JSONObject asJSON() throws Exception {
        //create a new JSON object
        JSONObject newJSONObject = new JSONObject();
        newJSONObject.put("username",this.getUsername());
        newJSONObject.put("password",this.password);

        //return the JSON object
        return  newJSONObject;
    }
}

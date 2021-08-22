package com.wapazockdemo.winterstoreconnector.interfaces;

public interface ConnectionInterface {
    void tokenReceived(String token);
    void connectionFailed(String error);
}

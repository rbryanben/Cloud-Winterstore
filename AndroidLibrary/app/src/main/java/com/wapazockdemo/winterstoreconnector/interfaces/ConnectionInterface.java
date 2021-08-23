package com.wapazockdemo.winterstoreconnector.interfaces;

import java.io.File;

public interface ConnectionInterface {
    void tokenReceived(String token);
    void connectionFailed(String error);
    void fileSaved(File file);
    void fileError(String error);
    void folderCreated(String id);
    void uploadResults(int uploadID, Boolean wasSuccessful,String result);
}

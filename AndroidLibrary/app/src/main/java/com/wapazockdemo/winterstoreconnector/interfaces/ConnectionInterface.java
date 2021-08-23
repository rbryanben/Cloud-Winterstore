package com.wapazockdemo.winterstoreconnector.interfaces;

import java.io.File;

public interface ConnectionInterface {
    void tokenReceived(String token);
    void connectionFailed(String error);
    void fileSaved(File file);
    void fileError(String error);
    void folderCreated(String id);
    void uploadResults(int uploadID, Boolean wasSuccessful,String result);
    void deleteResults(String indexObjectID,Boolean wasSuccessful, String result);
    void giveKeyResults(String account, Boolean wasSuccessful, String result);
    void removeKeysResults(String accounts, Boolean wasSuccessful,String result);
    void fileInfoResults(String file,Boolean wasSuccessful, String result);
    void getFolderResults(String folder,Boolean wasSuccessful, String result);
}

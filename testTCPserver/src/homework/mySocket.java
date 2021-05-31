package homework;

import java.net.*;

public class mySocket {
    String whichObject = "";
    Socket socket;
    
    public mySocket(Socket accept) {
        this.socket = accept;
    }
    
    public void getWhichObject(String object) {
        this.whichObject = object;
    }
    
}

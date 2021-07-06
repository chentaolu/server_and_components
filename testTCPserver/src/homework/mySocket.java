package homework;

import java.net.*;

public class mySocket {
    String component = "";
    Socket socket;
    
    public mySocket(Socket accept) {
        this.socket = accept;
    }
    
    public void setComponent(String component) {
        this.component = component;
    }
    
}

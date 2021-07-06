package homework;

import java.io.IOException;
import java.net.*;
import java.util.ArrayList;
import java.util.List;

public class server {
    
    static List<mySocket> sockets = new ArrayList<mySocket>();

    public static void main(String[] args) throws IOException {
    
        int port = 1278;
        ServerSocket ss = new ServerSocket(port);
        while(true) {
            try {
                Socket accept = ss.accept();
                int nowIndex = sockets.size();
                sockets.add(new mySocket(accept));
                Thread t = new Thread(new serverThread(accept, nowIndex));
                t.start();
            } catch (Exception e) {
                e.printStackTrace();
                ss.close();
            }
        }
    }
    /*
    public static mySocket getSocketByComponent () {
    	sockets.
    }*/
}

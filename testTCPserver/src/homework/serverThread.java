package homework;

import java.io.DataInputStream;
import java.io.IOException;
import java.net.*;

public class serverThread extends server implements Runnable {
    private Socket socket;
    String socketName;
    int index;
    
    public serverThread(Socket socket, int index){
        this.socket = socket;
        this.index = index;
    }
    
    public void run() {
        try {
          System.out.println("Just connect to " + socket.getRemoteSocketAddress());
          DataInputStream in = new DataInputStream(socket.getInputStream());
          System.out.flush();
          String object = in.readUTF();
          System.out.println(object);
          server.sockets.get(this.index).getWhichObject(object);
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        while(true) {
            try {
              DataInputStream in = new DataInputStream(socket.getInputStream());
              System.out.flush();
              System.out.println(socket.getRemoteSocketAddress() + " says " +in.readUTF());
            } catch (IOException e) {
              e.printStackTrace();
              break;
            }
          } 
    }
}

package homework;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.net.*;
import org.json.JSONObject;
import org.json.JSONException;

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
          BufferedReader recv = new BufferedReader(new InputStreamReader(socket.getInputStream()));
          System.out.flush();
          String object = recv.readLine();
          try {
              JSONObject jsonObject = new JSONObject(object);
              String component = jsonObject.getString("component");
              System.out.println(component);
        	  server.sockets.get(this.index).setComponent(component);
          } catch (JSONException jsonErr) {
        	  System.out.print(jsonErr.toString());
          }
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

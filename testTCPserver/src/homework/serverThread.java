package homework;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.BufferedReader;
import java.net.*;
import org.json.JSONObject;
import org.json.JSONException;

public class serverThread extends server implements Runnable {
    private Socket socket;
    String socketName;
    int index;
    PrintWriter out;
    BufferedReader recv;
    
    public serverThread(Socket socket, int index){
        this.socket = socket;
        this.index = index;
    }
    
    public void run() {
        try {
	        System.out.println("Just connect to " + socket.getRemoteSocketAddress());
	        recv = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	        out = new PrintWriter(socket.getOutputStream()); 
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
                String object = recv.readLine();
                try {
                    JSONObject jsonObject = new JSONObject(object);
                    String sendTo = jsonObject.getString("sendTo");
                    if (sendTo.equals("databaseConnector")) {
                    	for (mySocket socket : server.sockets) {
                    		if (socket.component.equals("databaseConnector")) {
                    			PrintWriter outToData = new PrintWriter(socket.socket.getOutputStream());
                    			outToData.println(object);
                    			outToData.flush();
                    		}
                    	}
                    } else if(sendTo.equals("player")) {
                    	for (mySocket socket : server.sockets) {
                    		if (socket.component.equals("player")) {
                    			PrintWriter outToData = new PrintWriter(socket.socket.getOutputStream());
                    			outToData.println(object);
                    			outToData.flush();
                    		}
                    	}
                    }
                } catch (JSONException jsonErr) {
              	  	System.out.print(jsonErr.toString());
                }
            } catch (IOException e) {
            	e.printStackTrace();
            	break;
            }
        } 
    }
}

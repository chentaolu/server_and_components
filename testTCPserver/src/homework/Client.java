package homework;

import java.net.*;
import java.io.*;
import java.util.Scanner;


public class Client {

	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);
		// TODO Auto-generated method stub
		String ServerName = "127.0.0.1";
		int port = 5678;
		String send;
		try {
			System.out.println("Connecting to " + ServerName + "and port : " + port);
			Socket client = new Socket(ServerName, port);
			System.out.println("Connect to" + client.getRemoteSocketAddress());
			OutputStream outToServer = client.getOutputStream();
			DataOutputStream out = new DataOutputStream(outToServer);
			
			out.writeUTF("HELLO FROM " + client.getLocalSocketAddress());
			send = scanner.nextLine();
			while(send.equals("quit") == false) {
				out.writeUTF(send);
				send = scanner.nextLine();
			}
			
			scanner.close();
			out.writeUTF(send);
			
			client.close();
		} catch(IOException e) {
			e.printStackTrace();
		}
	}

}

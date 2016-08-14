package test;


import java.io.*;
import java.net.Socket;
import java.net.SocketTimeoutException;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.zip.DataFormatException;

import javax.swing.JOptionPane;

/**
 * Created by daimin on 16/1/6.
 */
public class NetUtil {

	public static int C2S_SEND_CONT_PROTO = 0x0006;
	public static int S2C_SEND_CONT_PROTO = 0x1006;

	public static int C2S_LOGIN_PROTO = 0x0003;
	public static int S2C_LOGIN_PROTO = 0x1003;

	
    private PrintStream out;
    private ChatClient chatClient;

    public NetUtil(ChatClient chatClient){
        this.chatClient = chatClient;
    }

    public void connect() throws IOException {
//        Log.i("Base64.decode", new String(Base64.encode("hello, daimin".getBytes(), Base64.DEFAULT)));
        Socket client = new Socket("192.168.0.104", 5005);
        client.setSoTimeout(1000 * 300);
        client.setKeepAlive(true);
        //获取Socket的输出流，用来发送数据到服务端

        out = new PrintStream(client.getOutputStream());
        try{
            new MyThread(client).start();
        } finally {
            //如果构造函数建立起了连接，则关闭套接字，如果没有建立起连接，自然不用关闭
//            client.close(); //只关闭socket，其关联的输入输出流也会被关闭
//        	out.close();
        }


    }

    public void send(String str, int tid){
        try {
            out.write(SimpleCrypto.pack(CompressionTools.compress(SimpleCrypto.encode(str).getBytes()), tid));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static String readDataFromConsole(String prompt) {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String str = null;
        try {
            System.out.print(prompt);
            str = br.readLine();

        } catch (IOException e) {
            e.printStackTrace();
        }
        return str;
    }

    class MyThread extends Thread{
        Socket client = null;
        public MyThread(Socket client){
            this.client = client;
        }

        @Override
        public void run() {
            while(true){
                BufferedInputStream buf = null;
                try {
                    byte [] cbuf = new byte[4];
                    for(int i = 0; i < 4; i++){
                    	cbuf[i] = 0;
                    }
                    BufferedInputStream bufInputStream = new BufferedInputStream(client.getInputStream());
                    bufInputStream.read(cbuf, 0, 4);
                    ByteBuffer byteBuf = ByteBuffer.wrap(cbuf);
                    
                    System.out.println(Arrays.toString(byteBuf.array()));
                    
                    int t = byteBuf.getShort() & 0xFFFF;
                    int dataSize = byteBuf.getShort() & 0xFFFF;
                    
                    Log.i("dataSize", dataSize+"");
                    Log.i("dataType", "0x" + Integer.toHexString(t));
                    
                    byte [] cdatabuf = new byte[dataSize];
                    bufInputStream.read(cdatabuf, 0, dataSize);
                    System.out.println(Arrays.toString(cdatabuf));
                    String msg = SimpleCrypto.decode(new String(CompressionTools.decompress(cdatabuf), "utf-8"));
                    if(t == NetUtil.S2C_SEND_CONT_PROTO){
                    	NetUtil.this.chatClient.getTa().append(msg + "\n");
                    }else if(t == NetUtil.S2C_LOGIN_PROTO){
                    	System.out.println("Login Successed!!!!!!!");
                    	JOptionPane.showMessageDialog(NetUtil.this.chatClient, "登录成功", "INFO", JOptionPane.INFORMATION_MESSAGE);
                    	NetUtil.this.chatClient.setLoginCtrlVisible(false);
                    }else if(t > 0x8000){
                    	JOptionPane.showMessageDialog(NetUtil.this.chatClient, msg, "ERROR", JOptionPane.ERROR_MESSAGE); 
                    	System.out.println("ERROR:\t" + msg);
                    }
             
                    Thread.sleep(100);
                }catch (SocketTimeoutException ste){
                    ste.printStackTrace();
                }
                catch (IOException e) {
                    e.printStackTrace();
                } catch (DataFormatException e) {
                    e.printStackTrace();
                }
                catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

        }
    }



}

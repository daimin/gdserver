package test;

import java.net.*;
import java.io.*;
import java.awt.*;
import javax.swing.*;

import java.awt.event.*;

public class ChatClient extends JFrame {
	private DatagramSocket s;

	private InetAddress hostAddress;

	private byte[] buf = new byte[1000];

	// 定义数据包用来接受数据
	private JPanel pane;

	private JTextArea ta;

	private JScrollPane jsp;

	private JTextField tf;

	// private JButton btn;

	private boolean start;

	// private String str;
	private boolean send = false;

    private NetUtil netUtil;
    
    private JPanel loginpane;
    
    private JPanel findpane;

	private JTextField nametf;

	private JTextField passtf;
	
	private JTextField findtf;

    public JTextArea getTa(){
        return this.ta;
    }

	public void startWork() {
        try {
            netUtil = new NetUtil(this);
            netUtil.connect();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

	public static void main(String[] args) {
		new ChatClient().startWork();
	}

	public ChatClient() {
		super("聊天客户端");
		setSize(320, 400);
		setLocation(200, 200);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setResizable(false);
		pane = new JPanel(new BorderLayout());
		JPanel tpane = new JPanel();
		tf = new JTextField(27);
		tf.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent evt) {
				send = true;
                ChatClient.this.netUtil.send(tf.getText(), NetUtil.C2S_SEND_CONT_PROTO);
                tf.setText("");
                tf.setFocusable(true);
			}
		});

		tpane.add(tf);
		
		
		loginpane = new JPanel(new FlowLayout());

		nametf = new JTextField(10);
		passtf = new JTextField(10);
		JButton loginbtn = new JButton("登录");
		loginbtn.addActionListener(new LoginAction(this));
		loginpane.add(nametf);
		loginpane.add(passtf);
		loginpane.add(loginbtn);

		findpane = new JPanel(new FlowLayout());
		findtf = new JTextField(16);
		JButton findbtn = new JButton("查找好友");
		findbtn.addActionListener(new ActionListener(){

			@Override
			public void actionPerformed(ActionEvent e) {
				String sendMsg = ChatClient.this.getNametf().getText();
				ChatClient.this.getNetUtil().send(sendMsg, 3);
			}
			
		});
		findpane.add(findtf, FlowLayout.LEFT);
		findpane.add(findbtn);
		
		ta = new JTextArea();
		ta.setEditable(false);
        ta.setForeground(Color.BLUE);
        Font font = new Font("Default",Font.PLAIN, 10);
        ta.setFont(font);
		jsp = new JScrollPane(ta);
		pane.add(jsp, BorderLayout.CENTER);
		pane.add(tpane, BorderLayout.SOUTH);
		
		JPanel jfpane = new JPanel(new BorderLayout());
		jfpane.add(loginpane, BorderLayout.NORTH);
		jfpane.add(findpane, BorderLayout.SOUTH);
		
		pane.add(jfpane, BorderLayout.NORTH);
		
		loginpane.setVisible(true);
		findpane.setVisible(false);
		
		setContentPane(pane);
		setVisible(true);

	}
	
	public NetUtil getNetUtil() {
		return netUtil;
	}
	
	public JTextField getNametf() {
		return nametf;
	}

	public JTextField getPasstf() {
		return passtf;
	}
	
	public void setLoginCtrlVisible(boolean visible){
		loginpane.setVisible(visible);
		findpane.setVisible(!visible);
	}
	
}

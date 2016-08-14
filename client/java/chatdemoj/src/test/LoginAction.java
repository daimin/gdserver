package test;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class LoginAction implements ActionListener {

	ChatClient client;
	
	public LoginAction(ChatClient chatClient) {
		this.client = chatClient;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		String sendMsg = "{\"name\":\"" + client.getNametf().getText() +
				"\", \"passwd\": \"" + client.getPasstf().getText() + "\"}";
		
		this.client.getNetUtil().send(sendMsg, NetUtil.C2S_LOGIN_PROTO);
	}

}

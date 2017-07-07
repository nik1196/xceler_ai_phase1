package com.example.nikhil.cykabot;

/**
 * Created by Nikhil on 16-06-2017.
 */

public class ChatMessage {
    public String message;
    public Boolean isMe;
    public String getMessage(){
        return this.message;
    }
    public Boolean getIsMe(){
        return this.isMe;
    }
    public void setMessage(String message){
        this.message = message;
    }
    public void setIsMe(Boolean isMe){
        this.isMe = isMe;
    }
}

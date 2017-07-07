package com.example.nikhil.cykabot;

import android.app.Activity;
import android.content.Context;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.util.List;

/**
 * Created by Nikhil on 16-06-2017.
 */

public class ChatBoxAdapter extends BaseAdapter {
    private Activity context;
    private List<ChatMessage> messages;
    public ChatBoxAdapter (Activity context, List<ChatMessage> messages){
        this.context = context;
        this.messages = messages;
    }
    @Override
    //get number of messages
    public int getCount(){
        if(messages != null)
            return messages.size();
        return 0;
    }

    @Override
    //get a particular message
    public ChatMessage getItem(int position){
        if (messages != null)
            return messages.get(position);
        return null;
    }
    @Override
    public long getItemId(int position){
        return position;
    }

    //add a message to the adapter
    public void add(ChatMessage message) {
        messages.add(message);
    }

    //wrapper class for the view containing messages
    public static class ViewHolder {
        public TextView txtMessage;
        public LinearLayout content;
        public LinearLayout contentWithBG;
    }
    private ViewHolder createViewHolder(View v) {
        ViewHolder holder = new ViewHolder();
        holder.txtMessage = (TextView)v.findViewById(R.id.textView);
        holder.content = (LinearLayout) v.findViewById(R.id.linearlayout);
        holder.contentWithBG = (LinearLayout)v.findViewById(R.id.linearlayout2);
        return holder;
    }
    @Override
    public View getView(final int position, View convertView, ViewGroup parent){
        ViewHolder holder;
        ChatMessage chatMessage = getItem(position);
        LayoutInflater vi = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        if (convertView == null) {
            convertView = vi.inflate(R.layout.chatlist, null);
            holder = createViewHolder(convertView);
            convertView.setTag(holder);
        } else {
            holder = (ViewHolder) convertView.getTag();
        }

        boolean myMsg = chatMessage.getIsMe();
        setAlignment(holder, myMsg);
        holder.txtMessage.setText(chatMessage.getMessage());

        return convertView;
    }

    public void setAlignment(ViewHolder viewHolder, Boolean isMe){
        if(!isMe){
            viewHolder.contentWithBG.setBackgroundResource(R.drawable.botchat);
            LinearLayout.LayoutParams layoutParams = (LinearLayout.LayoutParams) viewHolder.contentWithBG.getLayoutParams();
            layoutParams.gravity = Gravity.LEFT;
            viewHolder.contentWithBG.setLayoutParams(layoutParams);

        }
        else {
            viewHolder.contentWithBG.setBackgroundResource(R.drawable.userchat);
            LinearLayout.LayoutParams layoutParams = (LinearLayout.LayoutParams) viewHolder.contentWithBG.getLayoutParams();
            layoutParams.gravity = Gravity.RIGHT;
            viewHolder.contentWithBG.setLayoutParams(layoutParams);


        }
    }
}

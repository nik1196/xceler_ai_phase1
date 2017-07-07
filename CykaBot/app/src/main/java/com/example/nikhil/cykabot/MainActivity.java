package com.example.nikhil.cykabot;

import android.Manifest;

import android.content.Context;
import android.content.pm.PackageManager;

import android.net.DhcpInfo;
import android.net.wifi.WifiManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.TextUtils;

import android.util.Log;

import android.view.View;

import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;

import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;

public class MainActivity extends AppCompatActivity {
    final int  MY_PERMISSIONS_REQUEST_USE_INTERNET  = 0;
    EditText inputText;;
    Button sendButton;
    LinearLayout linearLayout;

     RequestQueue requestQueue;

    ListView messageListView; //ListView to be populated with messages

    private ChatBoxAdapter adapter; //adapter for the ListView
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        inputText = (EditText) findViewById(R.id.editText); //box for the user to enter message
        sendButton = (Button) findViewById(R.id.button); //send sendButton
        linearLayout = (LinearLayout) findViewById(R.id.linearlayout);

        getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE); //readjust window when opening/closing keyboard

        //check for wifi permission, request permission if not granted
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.INTERNET) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.INTERNET}, MY_PERMISSIONS_REQUEST_USE_INTERNET);
        }


        messageListView = (ListView) findViewById(R.id.listview);
        adapter = new ChatBoxAdapter(MainActivity.this, new ArrayList<ChatMessage>());
        messageListView.setAdapter(adapter);

        WifiManager wifiManager = (WifiManager)this.getApplicationContext().getSystemService(Context.WIFI_SERVICE);
        DhcpInfo dhcpInfo = wifiManager.getDhcpInfo();
        String ipaddress = intToIp(dhcpInfo.ipAddress);

        Log.d("address", ipaddress);
        requestQueue = Volley.newRequestQueue(MainActivity.this);
        makeRequest("http://apacheHeli.pythonanywhere.com/", null, requestQueue); //connect to server to receive greeting
        //makeRequest("http://192.168.1.104:8000/", null, requestQueue);

        }
        String intToIp(int integer) {
            return (integer & 0xFF) + "." + ((integer >> 8) & 0xFF) + "."
                + ((integer >> 16) & 0xFF) + "." + (((integer >> 24) & 0xFF)-1);
        }

    //callback function for send button
    public void submit(View view){
        String messageText = inputText.getText().toString();
        if(!TextUtils.isEmpty(messageText)) {
            requestQueue = Volley.newRequestQueue(MainActivity.this);
            String url = "http://apacheHeli.pythonanywhere.com/input";
            //String url = "http://192.168.1.104:8000/input";

            Log.d("event", "before req");
            //create query in json format
            HashMap<String, String> hashMap = new HashMap<String, String>();
            hashMap.put("input", inputText.getText().toString());
            JSONObject jsonObject = new JSONObject(hashMap);
            makeRequest(url, jsonObject, requestQueue);

            ChatMessage chatMessage = new ChatMessage();
            chatMessage.setMessage(messageText);
            chatMessage.setIsMe(true);
            displayMessage(chatMessage);
            inputText.setText("");


        }
    }

    //send query to server and display the response
    public void makeRequest(String url, JSONObject jsonObject, final RequestQueue requestQueue){
        JsonObjectRequest jsObjRequest = new JsonObjectRequest
                (Request.Method.POST, url, jsonObject, new Response.Listener<JSONObject>() {

                    @Override
                    //display reply from server
                    public void onResponse(JSONObject response) {
                        Log.d("response", response.toString());
                        try{
                            String messageText = response.get("reply").toString();
                            ChatMessage chatMessage = new ChatMessage();
                            chatMessage.setMessage(messageText);
                            chatMessage.setIsMe(false);
                            displayMessage(chatMessage);

                        }
                        catch (JSONException e){
                            e.printStackTrace();
                        }
                        requestQueue.stop();
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // TODO Auto-generated method stub

                    }
                });


        Log.d("event", "making req");
        requestQueue.add(jsObjRequest); //add request to request queue
    }


    public void displayMessage(ChatMessage message) {
        adapter.add(message);
        adapter.notifyDataSetChanged();
        messageListView.setSelection(messageListView.getCount() - 1);
    }


    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSIONS_REQUEST_USE_INTERNET: {
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                } else {
                    Toast.makeText(getApplicationContext(), "Please provide internet permission", Toast.LENGTH_SHORT);
                    finish();
                }
                break;
            }

        }
    }
    }

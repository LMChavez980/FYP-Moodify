package com.fypmood.moodify;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.Window;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;
import com.spotify.sdk.android.auth.AuthorizationClient;
import com.spotify.sdk.android.auth.AuthorizationRequest;
import com.spotify.sdk.android.auth.AuthorizationResponse;

public class SplashActivity extends AppCompatActivity
{
    private RequestQueue queue;

    private static final int REQUEST_CODE = 1337;
    private static final String CLIENT_ID = "4110566732ad4c08b6f0e6c5768e552d";
    private static final String REDIRECT_URI = "com.fypmood.moodify://callback";
    private static final String SCOPES = "playlist-read-private, playlist-modify-public, playlist-modify-private";

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();
        setContentView(R.layout.activity_splash);

        AuthorizationRequest request = new AuthorizationRequest.Builder(CLIENT_ID, AuthorizationResponse.Type.TOKEN, REDIRECT_URI)
                .setShowDialog(false)
                .setScopes(new String[]{SCOPES})
                .setCampaign("your-campaign-token")
                .build();
        AuthorizationClient.openLoginActivity(this, REQUEST_CODE, request);

        queue = Volley.newRequestQueue(this);
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent){
        super.onActivityResult(requestCode, resultCode, intent);

        //Check if result comes from correct activity
        if(requestCode == REQUEST_CODE){
            AuthorizationResponse response = AuthorizationClient.getResponse(resultCode, intent);

            switch (response.getType()){
                case TOKEN:
                    //successful
                    String token = response.getAccessToken();
                    Log.d("SPLASH", "AUTH TOKEN ACQUIRED");
                    Intent intent_main = new Intent(SplashActivity.this, AddToPool.class);
                    intent_main.putExtra("TOKEN", token);
                    startActivity(intent_main);
                    break;

                case ERROR:
                    //handle error response
                    Log.e("SPLASH", "FAILED TO GET AUTH TOKEN");
                    break;

                default:
                    Log.d("SPLASH", "Cancelled Flow?");
            }
        }

    }


}

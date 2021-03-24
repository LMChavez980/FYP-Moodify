package com.fypmood.moodify;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.Window;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;
import com.spotify.sdk.android.auth.AuthorizationClient;
import com.spotify.sdk.android.auth.AuthorizationRequest;
import com.spotify.sdk.android.auth.AuthorizationResponse;

import kaaes.spotify.webapi.android.SpotifyApi;
import kaaes.spotify.webapi.android.SpotifyService;
import kaaes.spotify.webapi.android.models.UserPrivate;
import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;

public class SplashActivity extends AppCompatActivity
{
    private RequestQueue queue;

    private static final int REQUEST_CODE = 1337;
    private static final String CLIENT_ID = "4110566732ad4c08b6f0e6c5768e552d";
    private static final String REDIRECT_URI = "com.fypmood.moodify://callback";
    private static final String SCOPES = "user-library-read, playlist-read-private, playlist-modify-public, playlist-modify-private";
    private SpotifyApi api = new SpotifyApi();
    private SpotifyService service;
    private SharedPreferences mSharedPreferences;
    private SharedPreferences.Editor editor;


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
                    mSharedPreferences = getSharedPreferences("SPOTIFY", 0);
                    editor = mSharedPreferences.edit();
                    editor.putString("TOKEN", token);
                    getUserId(token);
                    editor.commit();
                    Intent intent_main = new Intent(SplashActivity.this, MainActivity.class);
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

    public void getUserId(String token){
        api.setAccessToken(token);
        service = api.getService();
        service.getMe(new Callback<UserPrivate>() {
            @Override
            public void success(UserPrivate userPrivate, Response response) {
                Log.d("SPLASH", "current user id: ".concat(userPrivate.id));
                editor.putString("USERID", userPrivate.id);
            }

            @Override
            public void failure(RetrofitError error) {
                Log.d("SPLASH", "Unable to get current user id");
            }
        });
    }


}